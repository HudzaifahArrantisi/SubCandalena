import asyncio
import re
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn
from rich import print as rprint
from ..database.manager import DBManager
from ..utils.wordlist import WordlistGenerator
from .passive import PassiveRecon
from .brute import BruteForce
from .analyzer import SubdomainAnalyzer
from ..utils.visualizer import Visualizer

console = Console()

class SubHunterXEngine:
    def __init__(self, domain: str, config: dict):
        self.domain = domain
        self.config = config
        self.db = DBManager()
        self.results = []
        self.live_count = 0
        self.scan_diff = {'new': [], 'removed': [], 'changed': []}
        self.scan_id = None
        
    async def full_scan(self):
        """Execute complete reconnaissance workflow"""
        rprint(f"\n[bold cyan]🚀 Starting FULL reconnaissance on {self.domain}[/]")
        previous_snapshot = self.db.snapshot(self.domain)
        
        # Phase 1: Passive Recon
        await self.phase_passive()
        
        # Phase 2: Brute Force
        await self.phase_brute()
        
        # Phase 3: Deep Analysis
        await self.phase_analysis()
        
        # Phase 4: Get all results from database
        self.results = self.db.get_all_subdomains(self.domain)
        self.scan_diff = self.db.diff_snapshots(previous_snapshot, self.db.snapshot(self.domain))
        high_risk = len([r for r in self.results if r.get('risk_level') == 'high' or (r.get('risk_score') or 0) >= 70])
        self.scan_id = self.db.create_scan_session(self.domain, len(self.results), high_risk)
        
        # Phase 5: Visualization (optional)
        if self.config.get("subhunterx", {}).get("auto_reports", False):
            self.visualize_results()
        
        rprint(f"\n[bold green]✅ Scan completed! Found {len(self.results)} live subdomains[/]")
        return self.results

    async def phase_passive(self):
        """Phase 1: Passive enumeration from 20+ sources"""
        rprint("\n[bold blue]📡 PHASE 1: Passive Reconnaissance[/]")
        
        passive = PassiveRecon(self.domain, self.config)
        passives = await passive.run_all_sources()
        
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn()
        ) as progress:
            task = progress.add_task("Saving passives...", total=len(passives))
            for sub in passives:
                self.db.save_subdomain({'domain': self.domain, 'subdomain': sub, 'source': 'passive'})
                progress.advance(task)
        
        rprint(f"[green]✅ Found {len(passives)} passive subdomains[/]")

    async def phase_brute(self):
        """Phase 2: Intelligent brute force with mutations"""
        rprint("\n[bold green]⚡ PHASE 2: Intelligent Brute Force[/]")
        
        wl_gen = WordlistGenerator(self.config)
        wordlist = wl_gen.generate_enhanced_wordlist(self.config['wordlists']['brute_size'])
        wordlist.extend(self.generate_permutation_words())
        wordlist = sorted(set(word.strip().lower() for word in wordlist if word and word.strip()))
        
        brute = BruteForce(self.domain, wordlist, self.config)
        lives = await brute.run_bruteforce()
        for subdomain in lives:
            self.db.save_subdomain({'domain': self.domain, 'subdomain': subdomain, 'source': 'bruteforce'})
        
        self.live_count += len(lives)
        rprint(f"[green]✅ Found {len(lives)} live subdomains[/]")

    async def phase_analysis(self):
        """Phase 3: Deep analysis & vulnerability assessment"""
        rprint("\n[bold magenta]🔬 PHASE 3: Deep Analysis & Vulnerability Assessment[/]")
        
        analyzer = SubdomainAnalyzer(self.config)
        all_subs = self.db.get_all_subdomains(self.domain)
        
        if not all_subs:
            rprint("[yellow]⚠ No subdomains to analyze[/]")
            return
        
        # Extract subdomain names from dict results
        subdomain_names = [sub.get('subdomain') if isinstance(sub, dict) else sub for sub in all_subs[:500]]
        subdomain_names = [s for s in subdomain_names if s]  # Filter None
        
        with ThreadPoolExecutor(max_workers=self.config['subhunterx']['threads']) as executor:
            futures = [executor.submit(analyzer.analyze, sub) for sub in subdomain_names]
            
            with Progress() as progress:
                task = progress.add_task("Analyzing...", total=len(futures))
                for future in futures:
                    try:
                        result = future.result()
                        if result and isinstance(result, dict) and result.get('subdomain'):
                            self.db.update_analysis(result)
                    except Exception as e:
                        pass
                    finally:
                        progress.advance(task)

    def visualize_results(self):
        """Create beautiful visualizations"""
        output_dir = self.config.get('subhunterx', {}).get('output_dir', 'reports')
        viz = Visualizer(self.results, self.domain, diff=self.scan_diff, output_dir=output_dir)
        viz.create_dashboard()

    def generate_permutation_words(self):
        """Generate simple mutation candidates from common environment patterns."""
        base_words = ['api', 'admin', 'app', 'web', 'portal']
        modifiers = ['dev', 'staging', 'test', 'prod', 'internal', 'v2']
        words = []
        for base in base_words:
            for modifier in modifiers:
                words.extend([f'{modifier}-{base}', f'{base}-{modifier}', f'{base}{modifier}'])
        return words
