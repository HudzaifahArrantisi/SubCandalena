#!/usr/bin/env python3
"""
SubCandalena - SubHunterX Pro v3.0
Advanced Subdomain Reconnaissance & Intelligence Suite
"""

from pyparsing import results
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
from rich.table import Table
from rich.text import Text
from rich import box

# Fix import paths
sys.path.insert(0, str(Path(__file__).parent))

try:
    from subhunterx.core.engine import SubHunterXEngine
    from subhunterx.utils.helpers import load_config, color_status
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
║                             SUBCANDALENA                                     ║
║        ADVANCED SUBDOMAIN RECONNAISSANCE & INTELLIGENCE SUITE                ║
╚══════════════════════════════════════════════════════════════════════════════╝
[/bold magenta]

[bold cyan]FEATURES:[/] [bold white]20+ SOURCES • AI MUTATIONS • DASHBOARD • API • DATABASE[/]
[bold yellow]POWERED BY:[/] [bold white]SUBCANDALENA INTELLIGENCE FRAMEWORK[/]
"""
    console.print(Panel(banner_text, border_style="bold red", padding=(1, 2)))


def render_results_table(results):
    formatted = []
    for item in results or []:
        if isinstance(item, dict):
            formatted.append(item)
        elif isinstance(item, str):
            formatted.append({"subdomain": item})

    if not formatted:
        console.print("[bold yellow]⚠ Tidak ada subdomain untuk ditampilkan.[/]")
        return

    table = Table(title="Subdomain Scan Results", box=box.SIMPLE_HEAVY)
    table.add_column("#", justify="right", style="dim", width=4)
    table.add_column("Subdomain", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center")
    table.add_column("Title", overflow="fold")
    table.add_column("Tech", overflow="fold")
    table.add_column("Risk", justify="center")

    for idx, sub in enumerate(sorted(formatted, key=lambda x: x.get("subdomain", "")), 1):
        status = color_status(sub.get("status_code"))
        title = sub.get("title") or "N/A"
        if len(title) > 60:
            title = f"{title[:57]}..."
        tech = sub.get("tech_stack") or "Unknown"
        if len(tech) > 40:
            tech = f"{tech[:37]}..."
        risk_score = sub.get("risk_score") or 0
        risk_level = sub.get("risk_level") or "low"
        risk_display = f"{risk_score} / {risk_level}"
        table.add_row(
            str(idx),
            sub.get("subdomain", "N/A"),
            status,
            title,
            tech,
            risk_display,
        )

    console.print(table)


async def main():
    parser = argparse.ArgumentParser(
        prog='python candalena.py',
        description=(
            'SubCandalena - subdomain reconnaissance scanner.\n'
            'Gunakan hanya untuk domain milik sendiri atau domain yang sudah punya izin untuk diuji.'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
[ Cara Pakai Awal ]
  python candalena.py -h
  python candalena.py example.com --quick

[ Contoh Scan ]
  python candalena.py example.com
      Scan normal dengan passive discovery, brute force, HTTP probe, dan risk analysis.

  python candalena.py example.com --quick
      Scan cepat untuk test awal. Wordlist lebih kecil dan screenshot dimatikan.

  python candalena.py example.com --threads 100
      Scan dengan concurrency lebih tinggi.

  python candalena.py example.com --dashboard
      Jalankan scan lalu buka dashboard lokal jika tersedia.

  python candalena.py example.com --export all
      Scan lalu simpan laporan ke HTML/JSON/CSV/TXT.

[ Output ]
  Hasil scan langsung tampil di terminal dalam bentuk tabel.
  Untuk file report, gunakan --export <html|json|csv|txt|all> (disimpan di folder reports/).

[ Catatan ]
  Edit config/config.yaml untuk timeout, retry, resolver, wordlist, rate limit, passive sources, dan output_dir.
        """
    )

    parser.add_argument('domain', help='Target domain, contoh: example.com')
    parser.add_argument('--dashboard', '-d', action='store_true',
                        help='Buka dashboard lokal setelah scan selesai')
    parser.add_argument('--threads', '-t', type=int, default=50,
                        help='Jumlah worker/concurrency scan (default: 50)')
    parser.add_argument('--quick', '-q', action='store_true',
                        help='Mode cepat untuk test awal: wordlist kecil dan screenshot off')
    parser.add_argument(
        '--export',
        choices=['html', 'json', 'csv', 'txt', 'all'],
        help='Simpan laporan ke file (default: tidak menyimpan file)'
    )

    args = parser.parse_args()

    # Validate domain
    if not re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', args.domain):
        console.print("[bold red]❌ INVALID DOMAIN FORMAT[/]")
        console.print("[bold yellow]USAGE: python candalena.py example.com --quick[/]")
        console.print("[bold yellow]HELP : python candalena.py -h[/]")
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
        high_risk = len([r for r in results if isinstance(r, dict) and ((r.get('risk_score') or 0) >= 70 or r.get('risk_level') == 'high')])

        # Generate reports
        console.print("\n[bold blue]📊 GENERATING REPORTS...[/]")
        visualizer = Visualizer(
            results,
            args.domain,
            diff=getattr(engine, 'scan_diff', None),
            output_dir=config.get('subhunterx', {}).get('output_dir', 'reports')
        )
        html_path = visualizer.create_dashboard()
        json_path = visualizer.export_json()
        csv_path = visualizer.export_csv()
        txt_path = visualizer.export_txt()

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
        if txt_path:
            console.print(f"   [bold green]✓[/] TXT: {txt_path}")

        if args.dashboard:
            console.print("\n[bold blue] LAUNCHING INTELLIGENCE DASHBOARD...[/]")
            asyncio.create_task(open_dashboard_task())

    except KeyboardInterrupt:
        console.print("\n[bold yellow]⏹ SCAN ABORTED BY OPERATOR[/]")
    except Exception as e:
        console.print(f"\n[bold red] FATAL ERROR:[/] {str(e)}")
        console.print("[bold yellow] TRY --quick OR CHECK requirements.txt[/]")


async def open_dashboard_task():
    await asyncio.sleep(2)
    try:
        import webbrowser
        webbrowser.open('http://127.0.0.1:8000')
        console.print("\n[bold cyan] DASHBOARD:[/] http://127.0.0.1:8000")
    except Exception:
        console.print("\n[bold cyan] MANUAL MODE:[/] python api_server.py")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[bold red]👋 TERMINATED — SUBCANDALENA OUT[/]")
