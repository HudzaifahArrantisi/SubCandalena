#!/usr/bin/env python3
"""
SubCandalena - SubHunterX Pro v3.0
Advanced Subdomain Reconnaissance & Intelligence Suite
"""

import argparse
import asyncio
import sys
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
    from subhunterx.modules.directory_scanner import DirectoryScanner
    from subhunterx.utils.helpers import load_config, color_status
    from subhunterx.database.manager import init_db
    from subhunterx.utils.asyncio_compat import configure_windows_event_loop
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

[bold cyan]FEATURES:[/] [bold white]20+ SOURCES • DASHBOARD • API • DATABASE[/]
[bold yellow]POWERED BY:[/] [bold white]Candalena INTELLIGENCE[/]
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


def render_results_list(results):
    subdomains = []
    for item in results or []:
        if isinstance(item, dict):
            subdomain = item.get("subdomain")
        else:
            subdomain = item
        if subdomain:
            subdomains.append(subdomain)

    if not subdomains:
        console.print("[bold yellow]⚠ Tidak ada subdomain untuk ditampilkan.[/]")
        return

    console.print("\n[bold cyan]SUBDOMAIN LIST[/]")
    for subdomain in sorted(set(subdomains)):
        console.print(subdomain)


def render_directory_table(results):
    if not results:
        console.print("\n[bold yellow]⚠ Tidak ada directory terbuka untuk ditampilkan.[/]")
        return

    table = Table(title="Directory Scan Results", box=box.SIMPLE_HEAVY)
    table.add_column("#", justify="right", style="dim", width=4)
    table.add_column("Host", style="cyan", overflow="fold")
    table.add_column("Path", style="magenta", overflow="fold")
    table.add_column("Status", justify="center")
    table.add_column("Size", justify="right")
    table.add_column("Type", overflow="fold")
    table.add_column("Title / Redirect", overflow="fold")

    for idx, item in enumerate(results, 1):
        status = color_status(item.get("status_code"))
        content_type = item.get("content_type") or "N/A"
        title = item.get("title") or item.get("location") or "N/A"
        if len(title) > 70:
            title = f"{title[:67]}..."
        table.add_row(
            str(idx),
            item.get("host", "N/A"),
            item.get("path", "N/A"),
            status,
            str(item.get("content_length", 0)),
            content_type,
            title,
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

  python candalena.py example.com -d
      Jalankan scan subdomain lalu scan directory/path umum pada host web yang hidup.

  python candalena.py example.com -o hasil.txt
      Jalankan scan lalu simpan subdomain ke file hasil.txt.

  python candalena.py example.com --export all
      Scan lalu simpan laporan ke HTML/JSON/CSV/TXT.

[ Output ]
  Default tanpa --dashboard, --export, atau -o akan tampil di terminal.
  Jika memakai -d/--directory-scan, terminal menampilkan tabel subdomain dan tabel directory secara terpisah.
  Gunakan --format list untuk output list sederhana atau --format table untuk tabel detail.
  Gunakan -o/--output <file.txt|file.json|file.csv|file.html> untuk output ke file tertentu.
  Gunakan --export <html|json|csv|txt|all> untuk report otomatis di folder reports/.

[ Catatan ]
  Edit config/config.yaml untuk timeout, retry, resolver, wordlist, rate limit, passive sources, dan output_dir.
        """
    )

    parser.add_argument('domain', help='Target domain, contoh: example.com')
    parser.add_argument('--dashboard', action='store_true',
                        help='Buka dashboard lokal setelah scan selesai')
    parser.add_argument('--directory-scan', '-d', action='store_true',
                        help='Scan directory/path umum pada semua subdomain web yang hidup')
    parser.add_argument('--directory-wordlist',
                        help='Path wordlist directory custom (default: data/wordlists/directories.txt)')
    parser.add_argument('--directory-limit', type=int,
                        help='Batasi jumlah path directory yang discan dari wordlist')
    parser.add_argument('--include-404', action='store_true',
                        help='Tampilkan hasil directory dengan status 404 juga')
    parser.add_argument('--threads', '-t', type=int, default=50,
                        help='Jumlah worker/concurrency scan (default: 50)')
    parser.add_argument('--quick', '-q', action='store_true',
                        help='Mode cepat untuk test awal: wordlist kecil dan screenshot off')
    parser.add_argument(
        '--export',
        choices=['html', 'json', 'csv', 'txt', 'all'],
        help='Simpan laporan ke file (default: tidak menyimpan file)'
    )
    parser.add_argument(
        '--output', '-o',
        help='Simpan hasil ke file tertentu. Format dideteksi dari ekstensi: .txt, .json, .csv, atau .html'
    )
    parser.add_argument(
        '--format',
        choices=['table', 'list'],
        default='table',
        help='Format output terminal saat tidak memakai --dashboard, --export, atau -o (default: table)'
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
        config.setdefault('directory_scan', {})['threads'] = 10
        config.setdefault('directory_scan', {})['limit'] = 20
        console.print("[bold yellow]⚡ QUICK MODE ENABLED[/]")

    config['subhunterx']['threads'] = args.threads
    if args.include_404:
        config.setdefault('directory_scan', {})['include_404'] = True

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

        console.print("\n[bold green]💀 SCAN COMPLETE — MISSION SUCCESS 💀[/]")
        console.print(f"[bold white]📊 TOTAL LIVE SUBDOMAINS:[/] [bold cyan]{len(results)}[/]")
        console.print(f"[bold white]🔥 HIGH RISK ASSETS:[/] [bold red]{high_risk}[/]")
        console.print(f"[bold white]💾 DATABASE:[/] [bold yellow]subhunterx_pro.db[/]")

        directory_results = []
        if args.directory_scan:
            console.print("\n[bold blue]📂 SCANNING DIRECTORIES...[/]")
            scanner = DirectoryScanner(config)
            directory_limit = args.directory_limit or config.get('directory_scan', {}).get('limit')
            directory_wordlist = args.directory_wordlist or config.get('directory_scan', {}).get('wordlist')
            directory_results = scanner.scan_results(
                results,
                wordlist_path=directory_wordlist,
                limit=directory_limit,
            )
            console.print(f"[bold white]📂 DIRECTORY FINDINGS:[/] [bold cyan]{len(directory_results)}[/]")

        visualizer = Visualizer(
            results,
            args.domain,
            diff=getattr(engine, 'scan_diff', None),
            output_dir=config.get('subhunterx', {}).get('output_dir', 'reports')
        )
        exported_paths = []

        if args.dashboard:
            console.print("\n[bold blue]📊 GENERATING DASHBOARD...[/]")
            html_path = visualizer.create_dashboard()
            if html_path:
                exported_paths.append(("HTML", html_path))
                open_dashboard(html_path)

        if args.output:
            console.print("\n[bold blue]💾 WRITING OUTPUT FILE...[/]")
            output_path = visualizer.export_to_path(args.output)
            if output_path:
                exported_paths.append(("OUTPUT", output_path))

        if args.export:
            console.print("\n[bold blue]📊 GENERATING REPORTS...[/]")
            export_actions = {
                'html': visualizer.create_dashboard,
                'json': visualizer.export_json,
                'csv': visualizer.export_csv,
                'txt': visualizer.export_txt,
            }
            selected_exports = export_actions.keys() if args.export == 'all' else [args.export]
            for export_type in selected_exports:
                path = export_actions[export_type]()
                if path:
                    exported_paths.append((export_type.upper(), path))

        if exported_paths:
            console.print("\n[bold cyan]📁 OUTPUT FILES:[/]")
            for label, path in exported_paths:
                console.print(f"   [bold green]✓[/] {label}: {path}")
        elif args.format == 'list':
            render_results_list(results)
        else:
            render_results_table(results)
            if args.directory_scan:
                render_directory_table(directory_results)

        if args.dashboard:
            console.print("\n[bold cyan]DASHBOARD MODE:[/] hasil scan dibuka sebagai HTML dashboard lokal.")

    except KeyboardInterrupt:
        console.print("\n[bold yellow]⏹ SCAN ABORTED BY OPERATOR[/]")
    except Exception as e:
        console.print(f"\n[bold red] FATAL ERROR:[/] {str(e)}")
        console.print("[bold yellow] TRY --quick OR CHECK requirements.txt[/]")


if __name__ == "__main__":
    try:
        configure_windows_event_loop()
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[bold red]👋 TERMINATED — SUBCANDALENA OUT[/]")
