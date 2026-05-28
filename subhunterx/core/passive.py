import aiohttp
import asyncio
import json
import os
import re
from typing import List, Set
from rich.console import Console

console = Console()


class PassiveRecon:
    SOURCES = {
        "crtsh": {
            "url": "https://crt.sh/?q=%.{domain}&output=json",
            "parser": lambda data: {
                name.strip().lower()
                for item in data
                for name in item.get("name_value", "").split("\n")
            }
        },
        "wayback": {
            "url": "https://web.archive.org/cdx?url=*.{domain}/*&output=json&fl=original&collapse=urlkey",
            "parser": lambda data: {
                re.sub(r"^https?://", "", row[0]).split("/")[0].split(":")[0].lower()
                for row in data[1:]
                if row
            }
        },
        "commoncrawl": {
            "url": "https://index.commoncrawl.org/CC-MAIN-2024-51-index?url=*.{domain}&output=json",
            "parser": lambda text: {
                re.sub(r"^https?://", "", json.loads(line).get("url", "")).split("/")[0].split(":")[0].lower()
                for line in text.splitlines()
                if line.strip()
            },
            "text": True
        },

        "urlscan": {
            "url": "https://urlscan.io/api/v1/search/?q=domain:{domain}",
            "parser": lambda data: {
                r["page"]["domain"].lower()
                for r in data.get("results", [])
                if "page" in r
            }
        },

        "threatcrowd": {
            "url": "https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}",
            "parser": lambda data: set(data.get("subdomains", []))
        },

        "hackertarget": {
            "url": "https://api.hackertarget.com/hostsearch/?q={domain}",
            "parser": lambda text: {
                line.split(",")[0].lower()
                for line in text.splitlines()
                if "," in line
            },
            "text": True
        },

        "alienvault": {
            "url": "https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns",
            "parser": lambda data: {
                entry["hostname"].lower()
                for entry in data.get("passive_dns", [])
            }
        },

        "bufferover": {
            "url": "https://dns.bufferover.run/dns?q=.{domain}",
            "parser": lambda data: {
                item.split(",")[1].lower()
                for item in data.get("FDNS_A", []) + data.get("RDNS", [])
                if "," in item
            }
        }
    }

    def __init__(self, domain: str, config: dict = None):
        self.domain = domain.lower().strip()
        self.config = config or {}
        self.results: Set[str] = set()

    async def run_all_sources(self) -> List[str]:
        timeout = aiohttp.ClientTimeout(total=self.config.get("subhunterx", {}).get("timeout", 20))
        headers = {
            "User-Agent": "PassiveRecon/1.0 (OSINT)"
        }

        async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
            enabled = self.config.get("passive_sources", {})
            tasks = [
                self.query_source(session, name, config)
                for name, config in self.SOURCES.items()
                if enabled.get(name, True)
            ]
            if enabled.get("github"):
                tasks.append(self.query_github(session))
            await asyncio.gather(*tasks, return_exceptions=True)

        return sorted(self._clean_results())

    async def query_source(self, session: aiohttp.ClientSession, name: str, config: dict):
        url = config["url"].format(domain=self.domain)

        try:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise Exception(f"HTTP {resp.status}")

                if config.get("text"):
                    raw = await resp.text()
                    subs = config["parser"](raw)
                else:
                    raw = await resp.json(content_type=None)
                    subs = config["parser"](raw)

                self.results.update(subs)
                console.print(f"[green]✓[/] {name}: {len(subs)} subs")

        except Exception as e:
            console.print(f"[red]✗[/] {name}: {str(e)[:60]}")

    async def query_github(self, session: aiohttp.ClientSession):
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            console.print("[yellow]-[/] github: skipped, GITHUB_TOKEN not set")
            return
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
        url = f"https://api.github.com/search/code?q=%22.{self.domain}%22"
        try:
            async with session.get(url, headers=headers) as resp:
                if resp.status != 200:
                    raise Exception(f"HTTP {resp.status}")
                data = await resp.json(content_type=None)
                found = set()
                for item in data.get("items", []):
                    text = f"{item.get('name', '')} {item.get('path', '')}"
                    found.update(re.findall(rf"([a-zA-Z0-9.-]+\.{re.escape(self.domain)})", text))
                self.results.update(found)
                console.print(f"[green]✓[/] github: {len(found)} subs")
        except Exception as e:
            console.print(f"[red]✗[/] github: {str(e)[:60]}")

    def _clean_results(self) -> Set[str]:
        """
        - hanya domain target
        - hapus wildcard
        - valid hostname
        """
        cleaned = set()

        for sub in self.results:
            sub = sub.replace("*.", "").strip().lower()
            if sub.endswith(self.domain) and self._is_valid_hostname(sub):
                cleaned.add(sub)

        return cleaned

    @staticmethod
    def _is_valid_hostname(hostname: str) -> bool:
        if len(hostname) > 253:
            return False
        regex = re.compile(
            r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$"
        )
        return bool(regex.match(hostname))
