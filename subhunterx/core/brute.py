import asyncio
import aiohttp
from typing import List
from rich.console import Console

console = Console()

class BruteForce:
    def __init__(self, domain: str, wordlist: List[str], config: dict):
        self.domain = domain
        self.wordlist = wordlist
        self.config = config
        self.live_subdomains = []

    async def run_bruteforce(self) -> List[str]:
        """High-performance async brute force"""
        semaphore = asyncio.Semaphore(self.config['subhunterx']['threads'])
        
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

    async def check_subdomain(self, session, semaphore, word: str):
        """Check single subdomain"""
        async with semaphore:
            subdomain = f"{word}.{self.domain}"
            
            for protocol in ['https', 'http']:
                try:
                    url = f"{protocol}://{subdomain}"
                    async with session.head(url, allow_redirects=False, ssl=False) as resp:
                        if resp.status in [200, 301, 302, 401, 403, 405]:
                            console.print(f"[green]LIVE[/] {subdomain} ({resp.status})")
                            return subdomain
                except:
                    pass
            
            await asyncio.sleep(self.config['rate_limit'])
            return None