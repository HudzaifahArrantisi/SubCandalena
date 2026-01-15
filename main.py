#!/usr/bin/env python3
"""
SubCandalena - SubHunterX Pro v3.0
Advanced Subdomain Reconnaissance & Intelligence Suite
"""

import argparse
import asyncio
import sys
import os
import re
from pathlib import Path

# Fix encoding for Windows
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Fix import paths
sys.path.insert(0, str(Path(__file__).parent))

try:
    from subhunterx.core.engine import SubHunterXEngine
    from subhunterx.utils.helpers import load_config
    from subhunterx.database.manager import init_db
    from subhunterx.utils.visualizer import open_dashboard, Visualizer
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("💡 Make sure all files are in correct folders!")
    sys.exit(1)

console = Console()


def banner():
    banner_text = """
[bold red]
███████╗██╗   ██╗██████╗   ██████╗ █████╗ ███╗   ██╗██████╗  █████╗ ██╗     ███████╗███╗   ██╗ █████╗
██╔════╝██║   ██║██╔══██╗ ██╔════╝██╔══██╗████╗  ██║██╔══██╗██╔══██╗██║     ██╔════╝████╗  ██║██╔══██╗
███████╗██║   ██║██████╔ ╝██║     ███████║██╔██╗ ██║██║  ██║███████║██║     █████╗  ██╔██╗ ██║███████║
╚════██║██║   ██║██╔══██  ██║     ██╔══██║██║╚██╗██║██║  ██║██╔══██║██║     ██╔══╝  ██║╚██╗██║██╔══██║
███████║╚██████╔╝██████╔╝ ╚██████╗██║  ██║██║ ╚████║██████╔╝██║  ██║███████╗███████╗██║ ╚████║██║  ██║
╚══════╝ ╚═════╝ ╚═════╝   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝
[/bold red]

[bold magenta]
╔══════════════════════════════════════════════════════════════════════════════╗
║                        ☠ SUBCANDALENA ☠                                    ║
║        ADVANCED SUBDOMAIN RECONNAISSANCE & INTELLIGENCE SUITE                ║
╚══════════════════════════════════════════════════════════════════════════════╝
[/bold magenta]

[bold cyan]FEATURES:[/] [bold white]20+ SOURCES • AI MUTATIONS • DASHBOARD • API • DATABASE[/]
[bold yellow]POWERED BY:[/] [bold white]SUBCANDALENA INTELLIGENCE FRAMEWORK[/]
"""
    console.print(Panel(banner_text, border_style="bold red", padding=(1, 2)))


async def main():
    parser = argparse.ArgumentParser(
        description='SubCandalena - SubHunterX Pro v3.0 | Advanced Subdomain Reconnaissance Suite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
[ SubCandalena Examples ]
  python main.py example.com
  python main.py example.com --dashboard
  python main.py example.com --threads 100
        """
    )

    parser.add_argument('domain', help='Target domain (e.g. example.com)')
    parser.add_argument('--dashboard', '-d', action='store_true',
                        help='Open web dashboard after scan')
    parser.add_argument('--threads', '-t', type=int, default=50,
                        help='Number of threads (default: 50)')
    parser.add_argument('--quick', '-q', action='store_true',
                        help='Quick scan (100 words, no screenshots)')

    args = parser.parse_args()

    # Validate domain
    if not re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', args.domain):
        console.print("[bold red]❌ INVALID DOMAIN FORMAT[/]")
        console.print("[bold yellow]USAGE: python main.py example.com[/]")
        return

    banner()

    # Load config & override
    config = load_config()
    if args.quick:
        config['subhunterx']['threads'] = 20
        config['wordlists']['brute_size'] = 100
        config['subhunterx']['screenshot'] = False
        console.print("[bold yellow]⚡ QUICK MODE ENABLED[/]")

    config['subhunterx']['threads'] = args.threads

    # Initialize database
    try:
        init_db()
        console.print("[bold green]✅ DATABASE INITIALIZED[/]")
    except Exception as e:
        console.print(f"[bold yellow]⚠ DATABASE WARNING:[/] {e}")

    # Start scan
    console.print(f"\n[bold cyan]🔍 TARGET LOCKED → {args.domain}[/]\n")

    try:
        engine = SubHunterXEngine(args.domain, config)
        results = await engine.full_scan()

        # Calculate high risk - handle None values
        high_risk = len([r for r in results if isinstance(r, dict) and (r.get('risk_score') or 0) > 70])

        # Generate reports
        console.print("\n[bold blue]📊 GENERATING REPORTS...[/]")
        visualizer = Visualizer(results, args.domain)
        html_path = visualizer.create_dashboard()
        json_path = visualizer.export_json()
        csv_path = visualizer.export_csv()

        console.print("\n[bold green]💀 SCAN COMPLETE — MISSION SUCCESS 💀[/]")
        console.print(f"[bold white]📊 TOTAL LIVE SUBDOMAINS:[/] [bold cyan]{len(results)}[/]")
        console.print(f"[bold white]🔥 HIGH RISK ASSETS:[/] [bold red]{high_risk}[/]")
        console.print(f"[bold white]💾 DATABASE:[/] [bold yellow]subhunterx_pro.db[/]")
        
        console.print("\n[bold cyan]📁 EXPORTED REPORTS:[/]")
        if html_path:
            console.print(f"   [bold green]✓[/] HTML: {html_path}")
        if json_path:
            console.print(f"   [bold green]✓[/] JSON: {json_path}")
        if csv_path:
            console.print(f"   [bold green]✓[/] CSV: {csv_path}")

        if args.dashboard:
            console.print("\n[bold blue]🌐 LAUNCHING INTELLIGENCE DASHBOARD...[/]")
            asyncio.create_task(open_dashboard_task())

    except KeyboardInterrupt:
        console.print("\n[bold yellow]⏹ SCAN ABORTED BY OPERATOR[/]")
    except Exception as e:
        console.print(f"\n[bold red]❌ FATAL ERROR:[/] {str(e)}")
        console.print("[bold yellow]💡 TRY --quick OR CHECK requirements.txt[/]")


async def open_dashboard_task():
    await asyncio.sleep(2)
    try:
        import webbrowser
        webbrowser.open('http://127.0.0.1:8000')
        console.print("\n[bold cyan]🌐 DASHBOARD:[/] http://127.0.0.1:8000")
    except Exception:
        console.print("\n[bold cyan]🌐 MANUAL MODE:[/] python api_server.py")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[bold red]👋 TERMINATED — SUBCANDALENA OUT[/]")
