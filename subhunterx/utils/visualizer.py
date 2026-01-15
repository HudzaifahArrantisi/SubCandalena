"""
SubCandalena - Professional HTML Report & Export Generator
Generates professional security reports with subdomain intelligence
"""

import json
import csv
from datetime import datetime
from pathlib import Path


class Visualizer:
    """
    Professional visualization and reporting for SubCandalena
    Generates HTML reports, JSON, and CSV exports
    """
    
    def __init__(self, results, domain):
        """Initialize visualizer with scan results"""
        self.results = results if results else []
        self.domain = domain
        self.timestamp = datetime.now()
    
    def create_dashboard(self):
        """
        Create professional HTML dashboard report
        Returns: Path to generated HTML file
        """
        html_content = self._generate_professional_html()
        
        # Create reports directory if it doesn't exist
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        # Generate filename with timestamp
        filename = f"SubCandalena_{self.domain.replace('.', '_')}_{self.timestamp.strftime('%Y%m%d_%H%M%S')}.html"
        filepath = reports_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"\n✅ HTML Report generated: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"❌ Error generating HTML report: {e}")
            return None
    
    def export_json(self):
        """Export results as JSON"""
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        filename = f"SubCandalena_{self.domain.replace('.', '_')}_{self.timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = reports_dir / filename
        
        # Prepare JSON data
        json_data = {
            "metadata": {
                "tool": "SubCandalena",
                "version": "3.0",
                "domain": self.domain,
                "scan_date": self.timestamp.isoformat(),
                "total_subdomains": len(self.results)
            },
            "subdomains": self._format_results_for_export_json()
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False, default=str)
            print(f"✅ JSON Export generated: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"❌ Error generating JSON export: {e}")
            return None
    
    def export_csv(self):
        """Export results as CSV"""
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        filename = f"SubCandalena_{self.domain.replace('.', '_')}_{self.timestamp.strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = reports_dir / filename
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Write headers
                writer.writerow([
                    'Index', 'Subdomain', 'Status Code', 'Title', 
                    'Tech Stack', 'Risk Score', 'Source', 'Discovery Date'
                ])
                
                # Write data rows
                for idx, sub in enumerate(self._format_results_for_export(), 1):
                    writer.writerow([
                        idx,
                        sub.get('subdomain', 'N/A'),
                        sub.get('status_code', 'N/A'),
                        sub.get('title', 'N/A'),
                        sub.get('tech_stack', 'N/A'),
                        sub.get('risk_score', 0),
                        sub.get('source', 'N/A'),
                        sub.get('created_at', 'N/A')
                    ])
            
            print(f"✅ CSV Export generated: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"❌ Error generating CSV export: {e}")
            return None
    
    def _format_results_for_export(self):
        """Format results for JSON and CSV export"""
        formatted = []
        for result in self.results:
            if isinstance(result, dict):
                formatted.append(result)
            elif isinstance(result, str):
                formatted.append({'subdomain': result})
        return sorted(formatted, key=lambda x: x.get('subdomain', ''))
    
    def _format_results_for_export_json(self):
        """Format results for JSON export with datetime handling"""
        formatted = []
        for result in self.results:
            if isinstance(result, dict):
                # Convert datetime to string
                item = result.copy()
                for key in item:
                    if hasattr(item[key], 'isoformat'):
                        item[key] = item[key].isoformat()
                formatted.append(item)
            elif isinstance(result, str):
                formatted.append({'subdomain': result})
        return sorted(formatted, key=lambda x: x.get('subdomain', ''))
    
    def _generate_professional_html(self):
        """Generate professional HTML report"""
        # Calculate statistics
        total = len(self.results)
        alive = sum(1 for r in self.results 
                   if isinstance(r, dict) and r.get('status_code') 
                   and 200 <= r.get('status_code', 0) < 400)
        high_risk = sum(1 for r in self.results 
                       if isinstance(r, dict) and (r.get('risk_score') or 0) > 7)
        
        scan_date = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        
        # Generate table rows
        table_rows_html = self._generate_table_rows_html()
        
        # Build HTML
        css_styles = self._get_css_styles()
        table_section = self._get_table_section(total, table_rows_html)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SubCandalena - Subdomain Reconnaissance Report</title>
    <style>
{css_styles}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🎯 SubCandalena</h1>
            <div class="subtitle">Advanced Subdomain Reconnaissance Report</div>
            <div class="meta">
                <strong>Target Domain:</strong> {self.domain}<br>
                <strong>Generated:</strong> {scan_date}<br>
                <strong>Total Subdomains:</strong> {total}
            </div>
        </div>
        
        <!-- Statistics -->
        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-number">{total}</span>
                <span class="stat-label">Total Subdomains</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{alive}</span>
                <span class="stat-label">Live Subdomains</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{high_risk}</span>
                <span class="stat-label">High Risk Assets</span>
            </div>
        </div>
        
        <!-- Summary -->
        <div class="section">
            <div class="summary-box">
                <p><strong>Scan Summary:</strong></p>
                <p>• Total subdomains discovered: <strong>{total}</strong></p>
                <p>• Live/Responsive subdomains: <strong>{alive}</strong></p>
                <p>• High-risk assets detected: <strong>{high_risk}</strong></p>
                <p>• Scanning completed on: <strong>{scan_date}</strong></p>
            </div>
        </div>
        
        <!-- All Subdomains -->
        <div class="section">
            <h2 class="section-title">📋 Discovered Subdomains ({total})</h2>
            {table_section}
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>Generated by <strong>SubCandalena v3.0</strong> - Advanced Subdomain Reconnaissance Suite</p>
            <p>Powered by SubCandalena Intelligence Framework</p>
            <p style="margin-top: 10px; font-size: 0.85em;">This report contains sensitive information. Handle with care.</p>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def _get_css_styles(self):
        """Get CSS styles for HTML report - Cyberpunk Theme"""
        return """        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --neon-cyan: #00ffff;
            --neon-pink: #ff006e;
            --neon-purple: #b01aff;
            --neon-green: #00ff41;
            --dark-bg: #0a0e27;
            --dark-card: #1a1f3a;
            --accent: #00ffff;
            --text-primary: #e0e0e0;
            --text-secondary: #a0a0a0;
        }
        
        @keyframes glow {
            0%, 100% { text-shadow: 0 0 10px var(--neon-cyan), 0 0 20px var(--neon-purple); }
            50% { text-shadow: 0 0 20px var(--neon-cyan), 0 0 30px var(--neon-pink); }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        @keyframes slideIn {
            from { transform: translateX(-100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        body {
            font-family: 'Courier New', 'Courier', monospace;
            background: linear-gradient(135deg, #0a0e27 0%, #1a0033 50%, #0a0e27 100%);
            min-height: 100vh;
            padding: 30px 20px;
            color: var(--text-primary);
            position: relative;
            overflow-x: hidden;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: repeating-linear-gradient(
                0deg,
                rgba(0, 255, 255, 0.03) 0px,
                transparent 1px,
                transparent 2px,
                rgba(0, 255, 255, 0.03) 3px
            );
            pointer-events: none;
            z-index: -1;
            animation: pulse 0.15s infinite;
        }
        
        .container {
            max-width: 1800px;
            margin: 0 auto;
            background: var(--dark-card);
            border-radius: 0;
            padding: 50px;
            box-shadow: 0 0 50px rgba(0, 255, 255, 0.3), inset 0 0 20px rgba(0, 0, 0, 0.5);
            border: 2px solid var(--neon-cyan);
            position: relative;
            animation: slideIn 0.8s ease-out;
        }
        
        .container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--neon-cyan), var(--neon-pink), transparent);
        }
        
        .header {
            text-align: center;
            margin-bottom: 50px;
            border-bottom: 3px double var(--neon-cyan);
            padding-bottom: 30px;
            position: relative;
        }
        
        .header::after {
            content: '';
            position: absolute;
            bottom: -3px;
            left: 50%;
            transform: translateX(-50%);
            width: 200px;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--neon-pink), transparent);
        }
        
        .header h1 {
            color: var(--neon-cyan);
            font-size: 3.5em;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 3px;
            font-weight: 900;
            animation: glow 3s ease-in-out infinite;
            text-shadow: 0 0 20px var(--neon-cyan);
        }
        
        .header .subtitle {
            color: var(--neon-pink);
            font-size: 1.4em;
            margin-bottom: 10px;
            letter-spacing: 2px;
            font-weight: bold;
        }
        
        .header .meta {
            color: var(--neon-green);
            font-size: 0.95em;
            margin-top: 15px;
            line-height: 1.8;
            background: rgba(0, 255, 65, 0.1);
            padding: 15px;
            border-left: 3px solid var(--neon-green);
            border-radius: 3px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 50px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(176, 26, 255, 0.1) 100%);
            border: 2px solid var(--neon-cyan);
            color: var(--text-primary);
            padding: 30px;
            border-radius: 0;
            text-align: center;
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.2), inset 0 0 15px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.2), transparent);
            transition: left 0.5s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 0 50px rgba(0, 255, 255, 0.5), inset 0 0 15px rgba(0, 0, 0, 0.3);
            border-color: var(--neon-pink);
        }
        
        .stat-card:hover::before {
            left: 100%;
        }
        
        .stat-number {
            font-size: 3.2em;
            font-weight: bold;
            margin-bottom: 12px;
            display: block;
            color: var(--neon-green);
            text-shadow: 0 0 10px var(--neon-green);
        }
        
        .stat-label {
            font-size: 0.9em;
            opacity: 0.8;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--neon-cyan);
        }
        
        .section {
            margin-bottom: 50px;
        }
        
        .section-title {
            color: var(--neon-pink);
            font-size: 2em;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 3px solid var(--neon-pink);
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: bold;
            text-shadow: 0 0 10px var(--neon-pink);
        }
        
        .subdomains-table {
            width: 100%;
            border-collapse: collapse;
            background: transparent;
            border-radius: 0;
            overflow: hidden;
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.15);
            border: 2px solid var(--neon-cyan);
        }
        
        .subdomains-table thead {
            background: linear-gradient(90deg, rgba(0, 255, 255, 0.15) 0%, rgba(176, 26, 255, 0.15) 100%);
            color: var(--neon-cyan);
            border-bottom: 3px solid var(--neon-pink);
        }
        
        .subdomains-table th {
            padding: 18px;
            text-align: left;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 2px;
            color: var(--neon-cyan);
        }
        
        .subdomains-table td {
            padding: 15px 18px;
            border-bottom: 1px solid rgba(0, 255, 255, 0.1);
            vertical-align: middle;
            color: var(--text-primary);
            font-size: 0.9em;
        }
        
        .subdomains-table tbody tr {
            transition: all 0.3s ease;
            background: rgba(0, 0, 0, 0.2);
        }
        
        .subdomains-table tbody tr:hover {
            background: rgba(0, 255, 255, 0.1);
            box-shadow: inset 0 0 10px rgba(0, 255, 255, 0.1);
        }
        
        .subdomains-table tbody tr:nth-child(odd) {
            background: rgba(176, 26, 255, 0.05);
        }
        
        .subdomain-name {
            font-family: 'Courier New', monospace;
            font-weight: 600;
            color: var(--neon-green);
            word-break: break-all;
            text-shadow: 0 0 5px var(--neon-green);
        }
        
        .status-code {
            font-family: 'Courier New', monospace;
            font-weight: 700;
            padding: 6px 12px;
            border-radius: 3px;
            font-size: 0.85em;
        }
        
        .status-200 { background: rgba(0, 255, 65, 0.2); color: var(--neon-green); border: 1px solid var(--neon-green); }
        .status-300 { background: rgba(255, 193, 7, 0.2); color: #ffc107; border: 1px solid #ffc107; }
        .status-400 { background: rgba(255, 0, 110, 0.2); color: var(--neon-pink); border: 1px solid var(--neon-pink); }
        .status-500 { background: rgba(255, 0, 0, 0.2); color: #ff4444; border: 1px solid #ff4444; }
        .status-na { background: rgba(160, 160, 160, 0.2); color: var(--text-secondary); border: 1px solid var(--text-secondary); }
        
        .risk-score {
            font-weight: 700;
            text-align: center;
            padding: 6px 12px;
            border-radius: 3px;
            font-size: 0.85em;
        }
        
        .risk-high { background: rgba(255, 0, 110, 0.2); color: var(--neon-pink); border: 1px solid var(--neon-pink); }
        .risk-medium { background: rgba(255, 193, 7, 0.2); color: #ffc107; border: 1px solid #ffc107; }
        .risk-low { background: rgba(0, 255, 65, 0.2); color: var(--neon-green); border: 1px solid var(--neon-green); }
        
        .footer {
            margin-top: 50px;
            padding-top: 30px;
            border-top: 3px double var(--neon-cyan);
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.9em;
        }
        
        .footer p {
            margin: 8px 0;
            letter-spacing: 1px;
        }
        
        .summary-box {
            background: rgba(0, 255, 255, 0.08);
            border-left: 4px solid var(--neon-green);
            border-right: 4px solid var(--neon-pink);
            border-top: 2px solid var(--neon-cyan);
            border-bottom: 2px solid var(--neon-purple);
            padding: 25px;
            border-radius: 0;
            margin-bottom: 25px;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.1);
        }
        
        .summary-box p {
            margin: 10px 0;
            color: var(--text-primary);
            line-height: 1.6;
        }
        
        .summary-box strong {
            color: var(--neon-green);
            text-shadow: 0 0 5px var(--neon-green);
        }
        
        .no-data {
            text-align: center;
            padding: 60px 40px;
            color: var(--text-secondary);
            font-size: 1.2em;
            background: rgba(0, 0, 0, 0.3);
            border: 2px dashed var(--neon-cyan);
            border-radius: 3px;
        }"""
    
    def _get_table_section(self, total, table_rows_html):
        """Get table section HTML"""
        if total == 0:
            return "<div class='no-data'>No subdomains discovered during this scan.</div>"
        else:
            return f"""<table class="subdomains-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Subdomain</th>
                        <th>Status</th>
                        <th>Title</th>
                        <th>Tech Stack</th>
                        <th>Risk Score</th>
                        <th>Source</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows_html}
                </tbody>
            </table>"""
    
    def _generate_table_rows_html(self):
        """Generate HTML table rows for all subdomains"""
        rows = []
        
        for idx, sub in enumerate(self.results, 1):
            if isinstance(sub, dict):
                subdomain_name = sub.get('subdomain', 'N/A')
                status_code = sub.get('status_code', 'N/A')
                title = sub.get('title', 'N/A')[:50] if sub.get('title') else 'N/A'
                tech = sub.get('tech_stack', 'N/A')[:30] if sub.get('tech_stack') else 'N/A'
                risk = sub.get('risk_score', 0)
                source = sub.get('source', 'Unknown')
            else:
                subdomain_name = sub
                status_code = 'N/A'
                title = 'N/A'
                tech = 'N/A'
                risk = 0
                source = 'N/A'
            
            # Determine status badge
            if status_code == 'N/A':
                status_badge = f'<span class="status-code status-na">{status_code}</span>'
            elif isinstance(status_code, int):
                if 200 <= status_code < 300:
                    status_badge = f'<span class="status-code status-200">{status_code}</span>'
                elif 300 <= status_code < 400:
                    status_badge = f'<span class="status-code status-300">{status_code}</span>'
                elif 400 <= status_code < 500:
                    status_badge = f'<span class="status-code status-400">{status_code}</span>'
                else:
                    status_badge = f'<span class="status-code status-500">{status_code}</span>'
            else:
                status_badge = f'<span class="status-code status-na">{status_code}</span>'
            
            # Risk score badge
            risk = risk if risk is not None else 0
            try:
                risk = int(risk)
            except (ValueError, TypeError):
                risk = 0
            
            if risk > 7:
                risk_badge = f'<span class="risk-score risk-high">{risk}/10</span>'
            elif risk > 4:
                risk_badge = f'<span class="risk-score risk-medium">{risk}/10</span>'
            else:
                risk_badge = f'<span class="risk-score risk-low">{risk}/10</span>'
            
            row_html = f"""                    <tr>
                        <td>{idx}</td>
                        <td><span class="subdomain-name">{subdomain_name}</span></td>
                        <td>{status_badge}</td>
                        <td>{title}</td>
                        <td>{tech}</td>
                        <td>{risk_badge}</td>
                        <td>{source}</td>
                    </tr>
"""
            rows.append(row_html)
        
        return "".join(rows)


def open_dashboard(filepath):
    """Open HTML dashboard in browser"""
    try:
        import webbrowser
        if Path(filepath).exists():
            webbrowser.open(f'file://{Path(filepath).resolve()}')
            print(f"✅ Dashboard opened: {filepath}")
            return True
    except Exception as e:
        print(f"⚠️ Could not open dashboard: {e}")
    return False
