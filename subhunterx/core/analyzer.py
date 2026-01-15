import requests
import re
import json
from urllib.parse import urlparse, parse_qs
from typing import Dict, Optional
import hashlib
from PIL import Image
import io

class SubdomainAnalyzer:
    TECH_SIGNATURES = {
        'wordpress': ['wp-content', 'wp-includes', '/wordpress/'],
        'jenkins': ['jenkins', '/login?from', 'X-Jenkins'],
        'grafana': ['grafana', '/login', 'Grafana'],
        'nginx': ['Server: nginx', 'nginx/'],
        'apache': ['Server: Apache', 'apache/']
    }

    def __init__(self, config: dict):
        self.config = config

    def analyze(self, subdomain: str) -> Optional[Dict]:
        """Full subdomain analysis"""
        try:
            url = f"https://{subdomain}"
            resp = requests.get(url, timeout=10, 
                              headers={'User-Agent': 'Mozilla/5.0'})
            
            tech_stack = self.detect_tech(resp)
            title = self.extract_title(resp.text)
            params = self.discover_params(url)
            risk_score = self.calculate_risk(subdomain, resp.status_code, params)
            
            screenshot_hash = self.capture_screenshot(url) if self.config['screenshot'] else None
            
            return {
                'subdomain': subdomain,
                'url': url,
                'status_code': resp.status_code,
                'title': title,
                'tech_stack': tech_stack,
                'parameters': params,
                'response_size': len(resp.content),
                'risk_score': risk_score,
                'screenshot_hash': screenshot_hash
            }
        except:
            return None

    def detect_tech(self, resp) -> str:
        """Detect technology stack"""
        techs = []
        text_lower = resp.text.lower()
        headers_lower = {k.lower(): v.lower() for k, v in resp.headers.items()}
        
        for tech, signatures in self.TECH_SIGNATURES.items():
            if any(sig in text_lower for sig in signatures) or \
               any(sig in headers_lower.get('server', '') for sig in signatures):
                techs.append(tech)
        
        return ', '.join(techs) or 'Unknown'

    def extract_title(self, html: str) -> str:
        match = re.search(r'<title[^>]*>([^<]+)', html, re.IGNORECASE | re.DOTALL)
        return match.group(1).strip()[:100] if match else "No Title"

    def discover_params(self, url: str) -> list:
        """Discover interesting parameters"""
        params = ['id', 'user', 'page', 'debug', 'admin', 'token', 'file', 'cmd']
        discovered = []
        
        for param in params:
            test_url = f"{url}?{param}=test"
            try:
                r = requests.get(test_url, timeout=5)
                if r.status_code < 400:
                    discovered.append(param)
            except:
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