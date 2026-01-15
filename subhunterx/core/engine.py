import asyncio
import aiohttp
import re
from subhunterx.database.manager import DBManager
from subhunterx.utils.wordlist import WordlistGenerator
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich import print as rprint
from datetime import datetime
import time
from typing import List, Dict
from ..utils.helpers import color_status
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
        
    async def full_scan(self):
        """Execute complete reconnaissance workflow"""
        rprint(f"\n[bold cyan]🚀 Starting FULL reconnaissance on {self.domain}[/]")
        
        # Phase 1: Passive Recon
        await self.phase_passive()
        
        # Phase 2: Brute Force
        await self.phase_brute()
        
        # Phase 3: Deep Analysis
        await self.phase_analysis()
        
        # Phase 4: Get all results from database
        self.results = self.db.get_all_subdomains(self.domain)
        
        # Phase 5: Visualization
        self.visualize_results()
        
        rprint(f"\n[bold green]✅ Scan completed! Found {len(self.results)} live subdomains[/]")
        return self.results

    async def phase_passive(self):
        """Phase 1: Passive enumeration from 20+ sources"""
        rprint("\n[bold blue]📡 PHASE 1: Passive Reconnaissance[/]")
        
        passive = PassiveRecon(self.domain)
        passives = await passive.run_all_sources()
        
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn()
        ) as progress:
            task = progress.add_task("Saving passives...", total=len(passives))
            for sub in passives:
                self.db.save_subdomain(sub, source='passive')
                progress.advance(task)
        
        rprint(f"[green]✅ Found {len(passives)} passive subdomains[/]")

    async def phase_brute(self):
        """Phase 2: Intelligent brute force with mutations"""
        rprint("\n[bold green]⚡ PHASE 2: Intelligent Brute Force[/]")
        
        wl_gen = WordlistGenerator(self.config)
        wordlist = wl_gen.generate_enhanced_wordlist(self.config['wordlists']['brute_size'])
        
        brute = BruteForce(self.domain, wordlist, self.config)
        lives = await brute.run_bruteforce()
        
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
        viz = Visualizer(self.results, self.domain)
        viz.create_dashboard()