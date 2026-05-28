import asyncio
import aiohttp
import socket
import uuid
from typing import List
from rich.console import Console

console = Console()

class BruteForce:
    def __init__(self, domain: str, wordlist: List[str], config: dict):
        self.domain = domain
        self.wordlist = wordlist
        self.config = config
        self.live_subdomains = []
        self.wildcard_ips = set()

    async def run_bruteforce(self) -> List[str]:
        """High-performance async brute force"""
        self.wildcard_ips = self.detect_wildcard_dns()
        concurrency = self.config['subhunterx'].get('concurrency') or self.config['subhunterx']['threads']
        semaphore = asyncio.Semaphore(concurrency)
        
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.config['subhunterx']['timeout']),
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        ) as session:
            tasks = [
                self.check_subdomain(session, semaphore, word)
                for word in self.wordlist
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            self.live_subdomains = [r for r in results if isinstance(r, str)]
        
        return self.live_subdomains

    def detect_wildcard_dns(self) -> set:
        """Resolve random hostnames to identify wildcard DNS responses."""
        found = set()
        for _ in range(2):
            random_host = f"{uuid.uuid4().hex[:12]}.{self.domain}"
            found.update(self.resolve_host(random_host))
        if found:
            console.print(f"[yellow]Wildcard DNS detected:[/] {', '.join(sorted(found))}")
        return found

    def resolve_host(self, hostname: str) -> List[str]:
        """Resolve hostname using system resolver, with optional dnspython resolvers."""
        resolvers = self.config.get('subhunterx', {}).get('resolvers') or []
        if resolvers:
            try:
                import dns.resolver
                resolver = dns.resolver.Resolver(configure=False)
                resolver.nameservers = resolvers
                return sorted({str(answer) for answer in resolver.resolve(hostname, 'A')})
            except Exception:
                return []
        try:
            return sorted({info[4][0] for info in socket.getaddrinfo(hostname, None, socket.AF_INET)})
        except Exception:
            return []

    async def check_subdomain(self, session, semaphore, word: str):
        """Check single subdomain"""
        async with semaphore:
            subdomain = f"{word}.{self.domain}"
            resolved_ips = set(self.resolve_host(subdomain))
            if not resolved_ips or (self.wildcard_ips and resolved_ips <= self.wildcard_ips):
                await asyncio.sleep(self.config['subhunterx'].get('rate_limit', self.config.get('rate_limit', 0.1)))
                return None
            
            for protocol in ['https', 'http']:
                try:
                    url = f"{protocol}://{subdomain}"
                    async with session.head(url, allow_redirects=False, ssl=False) as resp:
                        if resp.status in [200, 301, 302, 401, 403, 405]:
                            console.print(f"[green]LIVE[/] {subdomain} ({resp.status})")
                            return subdomain
                except:
                    pass
            
            await asyncio.sleep(self.config['subhunterx'].get('rate_limit', self.config.get('rate_limit', 0.1)))
            return None
