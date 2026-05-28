"""
SubCandalena HTML report and export generator.
"""

import csv
import html as html_lib
import json
from datetime import datetime
from pathlib import Path


class Visualizer:
    """
    Generate plain HTML reports, JSON exports, CSV exports, and TXT lists.
    """

    def __init__(self, results, domain, diff=None, output_dir="reports"):
        self.results = results if results else []
        self.domain = domain
        self.diff = diff or {"new": [], "removed": [], "changed": []}
        self.output_dir = output_dir
        self.timestamp = datetime.now()

    def create_dashboard(self):
        """Create an HTML report."""
        html_content = self._generate_professional_html()
        filepath = self._report_path("html")

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"\nHTML report generated: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"Error generating HTML report: {e}")
            return None

    def export_json(self):
        """Export results as JSON."""
        filepath = self._report_path("json")
        json_data = {
            "metadata": {
                "tool": "SubCandalena",
                "version": "3.0",
                "domain": self.domain,
                "scan_date": self.timestamp.isoformat(),
                "total_subdomains": len(self.results),
                "diff": self.diff,
            },
            "subdomains": self._format_results_for_export_json(),
        }

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False, default=str)
            print(f"JSON export generated: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"Error generating JSON export: {e}")
            return None

    def export_csv(self):
        """Export results as CSV."""
        filepath = self._report_path("csv")

        try:
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "Index",
                        "Subdomain",
                        "IP Address",
                        "Status Code",
                        "Title",
                        "Tech Stack",
                        "Server",
                        "CNAME",
                        "Source",
                        "Risk Score",
                        "Risk Level",
                        "Risk Reasons",
                    ]
                )

                for idx, sub in enumerate(self._format_results_for_export(), 1):
                    writer.writerow(
                        [
                            idx,
                            sub.get("subdomain", "N/A"),
                            sub.get("ip_address", "N/A"),
                            sub.get("status_code", "N/A"),
                            sub.get("title", "N/A"),
                            sub.get("tech_stack", "N/A"),
                            sub.get("server", "N/A"),
                            sub.get("cname", "N/A"),
                            sub.get("source", "N/A"),
                            sub.get("risk_score", 0),
                            sub.get("risk_level", "low"),
                            self._join_reasons(sub.get("risk_reasons", [])),
                        ]
                    )

            print(f"CSV export generated: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"Error generating CSV export: {e}")
            return None

    def export_txt(self):
        """Export a plain subdomain list."""
        filepath = self._report_path("txt")
        try:
            subdomains = [
                item.get("subdomain") if isinstance(item, dict) else item
                for item in self._format_results_for_export()
            ]
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("\n".join(sorted(sub for sub in subdomains if sub)))
            print(f"TXT export generated: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"Error generating TXT export: {e}")
            return None

    def _format_results_for_export(self):
        formatted = []
        for result in self.results:
            if isinstance(result, dict):
                formatted.append(result)
            elif isinstance(result, str):
                formatted.append({"subdomain": result})
        return sorted(formatted, key=lambda x: x.get("subdomain", ""))

    def _format_results_for_export_json(self):
        formatted = []
        for result in self._format_results_for_export():
            item = result.copy()
            for key in item:
                if hasattr(item[key], "isoformat"):
                    item[key] = item[key].isoformat()
            formatted.append(item)
        return formatted

    def _generate_professional_html(self):
        total = len(self.results)
        alive = sum(
            1
            for r in self.results
            if isinstance(r, dict)
            and r.get("status_code")
            and 200 <= r.get("status_code", 0) < 400
        )
        high_risk = sum(
            1
            for r in self.results
            if isinstance(r, dict)
            and (r.get("risk_level") == "high" or (r.get("risk_score") or 0) >= 70)
        )

        scan_date = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        table_rows_html = self._generate_table_rows_html()
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SubCandalena - Subdomain Reconnaissance Report</title>
    <style>{self._get_css_styles()}</style>
</head>
<body>
    <div class="container">
        <header class="report-header">
            <div>
                <p class="eyebrow">SubCandalena v3.0</p>
                <h1>Subdomain Reconnaissance Report</h1>
            </div>
            <div class="report-meta">
                <div><span>Target</span><strong>{self._escape(self.domain)}</strong></div>
                <div><span>Generated</span><strong>{scan_date}</strong></div>
            </div>
        </header>

        <div class="stats-grid">
            <div class="stat-card"><span class="stat-number">{total}</span><span class="stat-label">Total Subdomains</span></div>
            <div class="stat-card"><span class="stat-number">{alive}</span><span class="stat-label">Live Subdomains</span></div>
            <div class="stat-card"><span class="stat-number">{high_risk}</span><span class="stat-label">High Risk Assets</span></div>
        </div>

        <section class="section">
            <div class="summary-box">
                <h2>Summary</h2>
                <dl>
                    <div><dt>Total subdomains discovered</dt><dd>{total}</dd></div>
                    <div><dt>Live or responsive subdomains</dt><dd>{alive}</dd></div>
                    <div><dt>High-risk assets detected</dt><dd>{high_risk}</dd></div>
                    <div><dt>Scan completed</dt><dd>{scan_date}</dd></div>
                </dl>
            </div>
        </section>

        <section class="section">
            <h2 class="section-title">Source Breakdown</h2>
            <div class="table-wrap compact">
                <table class="subdomains-table">
                    <thead><tr><th>Source</th><th>Count</th></tr></thead>
                    <tbody>{self._source_breakdown_rows()}</tbody>
                </table>
            </div>
        </section>

        {self._generate_diff_section()}

        <section class="section">
            <h2 class="section-title">Discovered Subdomains ({total})</h2>
            <input class="table-filter" id="tableFilter" type="search" placeholder="Filter table">
            {self._get_table_section(total, table_rows_html)}
        </section>

        <footer class="footer">
            <p>Generated by SubCandalena. This report may contain sensitive reconnaissance data.</p>
        </footer>
    </div>
    <script>
        const filter = document.getElementById('tableFilter');
        if (filter) {{
            filter.addEventListener('input', function () {{
                const value = this.value.toLowerCase();
                document.querySelectorAll('.main-table tbody tr').forEach(function (row) {{
                    row.style.display = row.textContent.toLowerCase().includes(value) ? '' : 'none';
                }});
            }});
        }}
        document.querySelectorAll('th[data-sort]').forEach(function (th) {{
            th.addEventListener('click', function () {{
                const table = th.closest('table');
                const tbody = table.querySelector('tbody');
                const index = Array.from(th.parentNode.children).indexOf(th);
                Array.from(tbody.querySelectorAll('tr'))
                    .sort(function (a, b) {{
                        return a.children[index].textContent.localeCompare(b.children[index].textContent, undefined, {{numeric: true}});
                    }})
                    .forEach(function (row) {{ tbody.appendChild(row); }});
            }});
        }});
    </script>
</body>
</html>"""

    def _get_css_styles(self):
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --page-bg: #f5f6f8; --surface: #ffffff; --border: #d8dde6;
            --text: #1f2933; --muted: #64748b; --heading: #111827;
            --blue: #2563eb; --green: #137333; --yellow: #8a5a00;
            --red: #b42318; --gray: #475569;
        }
        body { font-family: Arial, Helvetica, sans-serif; background: var(--page-bg); min-height: 100vh; padding: 24px; color: var(--text); overflow-x: hidden; }
        .container { max-width: 1280px; margin: 0 auto; background: var(--surface); border: 1px solid var(--border); padding: 32px; }
        .report-header { display: flex; justify-content: space-between; gap: 24px; align-items: flex-start; margin-bottom: 28px; padding-bottom: 20px; border-bottom: 1px solid var(--border); }
        .eyebrow { color: var(--muted); font-size: 0.8rem; font-weight: 700; margin-bottom: 8px; text-transform: uppercase; }
        h1 { color: var(--heading); font-size: 1.8rem; line-height: 1.2; font-weight: 700; }
        .report-meta { min-width: 260px; border: 1px solid var(--border); }
        .report-meta div { display: flex; justify-content: space-between; gap: 16px; padding: 10px 12px; border-bottom: 1px solid var(--border); font-size: 0.9rem; }
        .report-meta div:last-child { border-bottom: 0; }
        .report-meta span { color: var(--muted); }
        .report-meta strong { color: var(--heading); text-align: right; word-break: break-word; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-bottom: 24px; }
        .stat-card { background: #fafafa; border: 1px solid var(--border); padding: 18px; }
        .stat-number { font-size: 2rem; font-weight: bold; margin-bottom: 6px; display: block; color: var(--heading); }
        .stat-label { font-size: 0.85rem; color: var(--muted); }
        .section { margin-bottom: 28px; }
        .section-title { color: var(--heading); font-size: 1.25rem; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid var(--border); font-weight: bold; }
        .table-wrap { overflow-x: auto; border: 1px solid var(--border); }
        .table-wrap.compact { max-width: 420px; }
        .table-filter { width: 100%; max-width: 320px; border: 1px solid var(--border); padding: 9px 10px; margin-bottom: 12px; font: inherit; }
        .subdomains-table { width: 100%; min-width: 980px; border-collapse: collapse; background: var(--surface); }
        .table-wrap.compact .subdomains-table { min-width: 0; }
        .subdomains-table thead { background: #f1f5f9; color: var(--heading); }
        .subdomains-table th { padding: 11px 12px; text-align: left; font-weight: 700; font-size: 0.8rem; color: var(--muted); border-bottom: 1px solid var(--border); cursor: default; }
        .subdomains-table th[data-sort] { cursor: pointer; }
        .subdomains-table td { padding: 10px 12px; border-bottom: 1px solid #eef2f7; vertical-align: middle; color: var(--text); font-size: 0.9rem; }
        .subdomains-table tbody tr:nth-child(even) { background: #fbfdff; }
        .subdomains-table tbody tr:hover { background: #f8fafc; }
        .subdomain-name { font-family: Consolas, 'Courier New', monospace; font-weight: 600; color: var(--blue); word-break: break-all; }
        .status-code, .risk-score { display: inline-block; min-width: 48px; padding: 4px 8px; border-radius: 3px; font-family: Consolas, 'Courier New', monospace; font-size: 0.8rem; font-weight: 700; text-align: center; }
        .risk-level { color: var(--muted); font-size: 0.82rem; margin-left: 6px; }
        .status-200, .risk-low { background: #e8f5e9; color: var(--green); border: 1px solid #b7dfbd; }
        .status-300, .risk-medium { background: #fff8e1; color: var(--yellow); border: 1px solid #f1d18a; }
        .status-400, .status-500, .risk-high { background: #fff1f0; color: var(--red); border: 1px solid #f3b7b3; }
        .status-na { background: #f1f5f9; color: var(--gray); border: 1px solid #d6dee8; }
        .footer { margin-top: 28px; padding-top: 18px; border-top: 1px solid var(--border); color: var(--muted); font-size: 0.85rem; }
        .summary-box { background: #fbfdff; border: 1px solid var(--border); padding: 18px; }
        .summary-box h2 { font-size: 1rem; color: var(--heading); margin-bottom: 12px; }
        .summary-box dl { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }
        .summary-box div { border-top: 1px solid #e8edf4; padding-top: 10px; }
        .summary-box dt { color: var(--muted); font-size: 0.82rem; margin-bottom: 4px; }
        .summary-box dd { color: var(--heading); font-weight: 700; }
        .no-data { text-align: center; padding: 36px 24px; color: var(--muted); font-size: 1rem; background: #fbfdff; border: 1px dashed var(--border); }
        @media (max-width: 760px) {
            body { padding: 12px; }
            .container { padding: 18px; }
            .report-header { display: block; }
            .report-meta { margin-top: 16px; min-width: 0; }
        }"""

    def _get_table_section(self, total, table_rows_html):
        if total == 0:
            return "<div class='no-data'>No subdomains discovered during this scan.</div>"

        return f"""<div class="table-wrap">
                <table class="subdomains-table main-table">
                    <thead>
                        <tr>
                            <th data-sort>#</th>
                            <th data-sort>Subdomain</th>
                            <th data-sort>IP</th>
                            <th data-sort>Status</th>
                            <th data-sort>Title</th>
                            <th data-sort>Tech</th>
                            <th data-sort>Server</th>
                            <th data-sort>CNAME</th>
                            <th data-sort>Source</th>
                            <th data-sort>Risk</th>
                            <th>Risk Reasons</th>
                        </tr>
                    </thead>
                    <tbody>{table_rows_html}</tbody>
                </table>
            </div>"""

    def _generate_table_rows_html(self):
        rows = []
        for idx, sub in enumerate(self._format_results_for_export(), 1):
            subdomain_name = sub.get("subdomain", "N/A")
            risk_reasons = self._join_reasons(sub.get("risk_reasons", []))
            row_html = f"""<tr>
                <td>{idx}</td>
                <td><span class="subdomain-name">{self._escape(subdomain_name)}</span></td>
                <td>{self._escape(sub.get("ip_address", "N/A") or "N/A")}</td>
                <td>{self._status_badge(sub.get("status_code", "N/A"))}</td>
                <td>{self._escape((sub.get("title") or "N/A")[:70])}</td>
                <td>{self._escape((sub.get("tech_stack") or "N/A")[:50])}</td>
                <td>{self._escape(sub.get("server", "N/A") or "N/A")}</td>
                <td>{self._escape(sub.get("cname", "N/A") or "N/A")}</td>
                <td>{self._escape(sub.get("source", "Unknown") or "Unknown")}</td>
                <td>{self._risk_badge(sub.get("risk_score", 0))} <span class="risk-level">{self._escape(sub.get("risk_level", "low") or "low")}</span></td>
                <td>{self._escape(risk_reasons)}</td>
            </tr>"""
            rows.append(row_html)
        return "".join(rows)

    def _status_badge(self, status_code):
        escaped_status = self._escape(status_code)
        if status_code == "N/A" or status_code is None:
            return f'<span class="status-code status-na">{escaped_status}</span>'
        try:
            status = int(status_code)
        except (TypeError, ValueError):
            return f'<span class="status-code status-na">{escaped_status}</span>'
        if 200 <= status < 300:
            status_class = "status-200"
        elif 300 <= status < 400:
            status_class = "status-300"
        elif 400 <= status < 500:
            status_class = "status-400"
        else:
            status_class = "status-500"
        return f'<span class="status-code {status_class}">{status}</span>'

    def _risk_badge(self, risk):
        try:
            risk = int(risk if risk is not None else 0)
        except (ValueError, TypeError):
            risk = 0
        if risk >= 70:
            risk_class = "risk-high"
        elif risk >= 35:
            risk_class = "risk-medium"
        else:
            risk_class = "risk-low"
        return f'<span class="risk-score {risk_class}">{risk}</span>'

    def _source_breakdown_rows(self):
        counts = {}
        for item in self._format_results_for_export():
            source = item.get("source") or "Unknown"
            counts[source] = counts.get(source, 0) + 1
        if not counts:
            return "<tr><td colspan='2'>No source data</td></tr>"
        return "".join(
            f"<tr><td>{self._escape(source)}</td><td>{count}</td></tr>"
            for source, count in sorted(counts.items())
        )

    def _generate_diff_section(self):
        new_count = len(self.diff.get("new", []))
        removed_count = len(self.diff.get("removed", []))
        changed_count = len(self.diff.get("changed", []))
        if new_count == 0 and removed_count == 0 and changed_count == 0:
            return ""
        rows = []
        for item in self.diff.get("new", [])[:50]:
            rows.append(f"<tr><td>New</td><td>{self._escape(item.get('subdomain'))}</td><td></td></tr>")
        for item in self.diff.get("removed", [])[:50]:
            rows.append(f"<tr><td>Removed</td><td>{self._escape(item.get('subdomain'))}</td><td></td></tr>")
        for item in self.diff.get("changed", [])[:50]:
            detail = f"status {item.get('old_status')} -> {item.get('new_status')}; risk {item.get('old_risk')} -> {item.get('new_risk')}"
            rows.append(f"<tr><td>Changed</td><td>{self._escape(item.get('subdomain'))}</td><td>{self._escape(detail)}</td></tr>")
        return f"""<section class="section">
            <h2 class="section-title">New / Removed / Changed Subdomains</h2>
            <div class="table-wrap">
                <table class="subdomains-table">
                    <thead><tr><th>Type</th><th>Subdomain</th><th>Detail</th></tr></thead>
                    <tbody>{''.join(rows)}</tbody>
                </table>
            </div>
        </section>"""

    def _join_reasons(self, reasons):
        if isinstance(reasons, list):
            return "; ".join(str(reason) for reason in reasons)
        return str(reasons or "")

    def _report_path(self, extension):
        reports_dir = Path(self.output_dir)
        reports_dir.mkdir(exist_ok=True)
        filename = f"SubCandalena_{self.domain.replace('.', '_')}_{self.timestamp.strftime('%Y%m%d_%H%M%S')}.{extension}"
        return reports_dir / filename

    def _escape(self, value):
        return html_lib.escape(str(value))


def open_dashboard(filepath):
    """Open HTML dashboard in browser."""
    try:
        import webbrowser

        if Path(filepath).exists():
            webbrowser.open(f"file://{Path(filepath).resolve()}")
            print(f"Dashboard opened: {filepath}")
            return True
    except Exception as e:
        print(f"Could not open dashboard: {e}")
    return False
