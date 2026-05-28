"""
Directory scanner for discovered HTTP subdomains.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, Iterable, List
from urllib.parse import urljoin, urlparse
from uuid import uuid4

import requests


class DirectoryScanner:
    """Scan common directories on discovered web hosts."""

    DEFAULT_WORDLIST = Path("data/wordlists/directories.txt")

    def __init__(self, config: dict):
        self.config = config
        self.scan_config = config.get("subhunterx", config)
        directory_config = config.get("directory_scan", {})
        self.timeout = directory_config.get("timeout", self.scan_config.get("timeout", 8))
        self.threads = directory_config.get("threads", min(self.scan_config.get("threads", 20), 30))
        self.include_404 = directory_config.get("include_404", False)
        self.user_agent = directory_config.get("user_agent", "SubCandalena-DirectoryScanner/1.0")
        self._baselines = {}

    def scan_results(self, subdomains: Iterable[dict], wordlist_path: str = None, limit: int = None) -> List[Dict]:
        """Scan directory paths across analyzed subdomain results."""
        bases = self._extract_base_urls(subdomains)
        paths = self.load_wordlist(wordlist_path)
        if limit:
            paths = paths[:limit]

        jobs = [(base, path) for base in bases for path in paths]
        if not jobs:
            return []

        self._baselines = self._build_baselines(bases)
        findings = []
        with ThreadPoolExecutor(max_workers=max(1, self.threads)) as executor:
            futures = [executor.submit(self._probe_path, base, path) for base, path in jobs]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    findings.append(result)

        return sorted(findings, key=lambda item: (item["host"], item["status_code"], item["path"]))

    def load_wordlist(self, wordlist_path: str = None) -> List[str]:
        """Load a directory wordlist from disk."""
        path = Path(wordlist_path) if wordlist_path else self.DEFAULT_WORDLIST
        if not path.exists():
            return []

        words = []
        with open(path, "r", encoding="utf-8") as handle:
            for line in handle:
                word = line.strip()
                if word and not word.startswith("#"):
                    words.append(word.lstrip("/"))
        return sorted(set(words))

    def _extract_base_urls(self, subdomains: Iterable[dict]) -> List[str]:
        bases = set()
        for item in subdomains or []:
            if not isinstance(item, dict):
                continue
            status_code = item.get("status_code")
            url = item.get("url")
            if status_code is None or not url:
                continue
            parsed = urlparse(url)
            if parsed.scheme and parsed.netloc:
                bases.add(f"{parsed.scheme}://{parsed.netloc}/")
        return sorted(bases)

    def _probe_path(self, base_url: str, path: str) -> Dict:
        url = urljoin(base_url, path)
        try:
            response = requests.get(
                url,
                timeout=self.timeout,
                headers={"User-Agent": self.user_agent},
                allow_redirects=False,
            )
        except requests.RequestException:
            return {}

        if response.status_code == 404 and not self.include_404:
            return {}

        title = self._extract_title(response.text)
        if not self.include_404 and self._looks_like_baseline(base_url, response, title):
            return {}

        return {
            "host": urlparse(base_url).netloc,
            "path": "/" + path.strip("/"),
            "url": url,
            "status_code": response.status_code,
            "content_length": len(response.content),
            "content_type": response.headers.get("Content-Type", "N/A"),
            "location": response.headers.get("Location", ""),
            "title": title,
        }

    def _build_baselines(self, bases: Iterable[str]) -> Dict[str, Dict]:
        baselines = {}
        for base_url in bases:
            random_path = f"__subcandalena_missing_{uuid4().hex}"
            url = urljoin(base_url, random_path)
            try:
                response = requests.get(
                    url,
                    timeout=self.timeout,
                    headers={"User-Agent": self.user_agent},
                    allow_redirects=False,
                )
            except requests.RequestException:
                continue

            baselines[base_url] = {
                "status_code": response.status_code,
                "content_length": len(response.content),
                "title": self._extract_title(response.text),
            }
        return baselines

    def _looks_like_baseline(self, base_url: str, response: requests.Response, title: str) -> bool:
        baseline = self._baselines.get(base_url)
        if not baseline:
            return False

        size_delta = abs(len(response.content) - baseline["content_length"])
        return (
            response.status_code == baseline["status_code"]
            and size_delta <= 64
            and title == baseline["title"]
        )

    @staticmethod
    def _extract_title(html: str) -> str:
        import html as html_lib
        import re

        match = re.search(r"<title[^>]*>([^<]+)", html, re.IGNORECASE | re.DOTALL)
        return html_lib.unescape(match.group(1).strip())[:80] if match else ""
