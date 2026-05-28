import requests
import re
import html as html_lib
from typing import Dict, Optional
import hashlib
from PIL import Image
import io

class SubdomainAnalyzer:
    TECH_SIGNATURES = {
        'wordpress': ['wp-content', 'wp-includes', '/wordpress/'],
        'jenkins': ['jenkins', '/login?from', 'X-Jenkins'],
        'grafana': ['grafana', 'grafana_session'],
        'plesk': ['plesk', 'login_up.php', 'Plesk Obsidian'],
        'nginx': ['Server: nginx', 'nginx/'],
        'apache': ['Server: Apache', 'apache/']
    }

    def __init__(self, config: dict):
        self.config = config
        self.scan_config = config.get('subhunterx', config)

    def analyze(self, subdomain: str) -> Optional[Dict]:
        """Full subdomain analysis"""
        last_error = None
        timeout = self.scan_config.get('timeout', 10)

        for scheme in ('https', 'http'):
            url = f"{scheme}://{subdomain}"
            try:
                resp = requests.get(
                    url,
                    timeout=timeout,
                    headers={'User-Agent': 'Mozilla/5.0'},
                    allow_redirects=True,
                )

                tech_stack = self.detect_tech(resp)
                title = self.extract_title(resp.text)
                params = self.discover_params(url)
                risk_score = self.calculate_risk(subdomain, resp.status_code, params)
                risk_level = self.risk_level(risk_score)

                screenshot_hash = (
                    self.capture_screenshot(resp.url)
                    if self.scan_config.get('screenshot', False)
                    else None
                )

                return {
                    'subdomain': subdomain,
                    'url': resp.url,
                    'status_code': resp.status_code,
                    'title': title,
                    'tech_stack': tech_stack,
                    'parameters': params,
                    'server': resp.headers.get('Server'),
                    'content_type': resp.headers.get('Content-Type'),
                    'response_size': len(resp.content),
                    'risk_score': risk_score,
                    'risk_level': risk_level,
                    'screenshot_hash': screenshot_hash
                }
            except requests.RequestException as exc:
                last_error = exc

        return {
            'subdomain': subdomain,
            'url': None,
            'status_code': None,
            'title': None,
            'tech_stack': 'Unknown',
            'parameters': [],
            'response_size': None,
            'risk_score': 0,
            'risk_level': 'low',
            'risk_reasons': [f'HTTP probe failed: {last_error}'] if last_error else []
        }

    def detect_tech(self, resp) -> str:
        """Detect technology stack"""
        techs = []
        text_lower = resp.text.lower()
        headers_text = " ".join(f"{key}: {value}" for key, value in resp.headers.items()).lower()

        for tech, signatures in self.TECH_SIGNATURES.items():
            if any(sig.lower() in text_lower or sig.lower() in headers_text for sig in signatures):
                techs.append(tech)

        return ', '.join(sorted(set(techs))) or 'Unknown'

    def extract_title(self, html_text: str) -> str:
        match = re.search(r'<title[^>]*>([^<]+)', html_text, re.IGNORECASE | re.DOTALL)
        return html_lib.unescape(match.group(1).strip())[:100] if match else "No Title"

    def discover_params(self, url: str) -> list:
        """Discover interesting parameters"""
        timeout = self.scan_config.get('timeout', 8)
        params = ['id', 'user', 'page', 'debug', 'admin', 'token', 'file', 'cmd']
        discovered = []

        for param in params:
            test_url = f"{url}?{param}=test"
            try:
                r = requests.get(test_url, timeout=timeout)
                if r.status_code < 400:
                    discovered.append(param)
            except requests.RequestException:
                pass
        return discovered

    def calculate_risk(self, subdomain: str, status: int, params: list) -> int:
        """ML-inspired risk scoring"""
        try:
            score = 0

            # Status-based scoring
            if status == 200: score += 30
            elif status in [401, 403]: score += 50

            # Path-based scoring
            risky_paths = ['admin', 'login', 'api', 'db', 'backup', 'config']
            if any(path in subdomain.lower() for path in risky_paths):
                score += 40

            # Parameter scoring
            if len(params) > 2: score += 20
            if 'debug' in params or 'cmd' in params: score += 30

            return min(max(int(score), 0), 100)
        except Exception:
            return 0

    @staticmethod
    def risk_level(score: int) -> str:
        if score >= 70:
            return 'high'
        if score >= 35:
            return 'medium'
        return 'low'

    def capture_screenshot(self, url: str) -> str:
        """Capture screenshot (requires selenium)"""
        try:
            from selenium import webdriver
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            driver.set_window_size(1920, 1080)
            driver.get(url)
            screenshot = driver.get_screenshot_as_png()
            driver.quit()
            
            # Hash for deduplication
            img = Image.open(io.BytesIO(screenshot))
            hash_md5 = hashlib.md5(screenshot).hexdigest()
            
            # Save screenshot
            img.save(f"data/screenshots/{hash_md5}.png")
            return hash_md5
        except:
            return None
