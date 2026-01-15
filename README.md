# 🎯 SubCandalena - SubHunterX Pro v3.0

<div align="center">

![Version](https://img.shields.io/badge/version-3.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**🚀 Enterprise-Grade Subdomain Reconnaissance & Intelligence Suite 🚀**

*Advanced subdomain enumeration tool with 20+ passive sources, intelligent brute force, AI-powered mutations, real-time dashboard, REST API, and vulnerability assessment.*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Configuration](#-configuration) • [API Documentation](#-api-documentation) • [Tutorials](#-tutorials)

</div>

---

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [✨ Features](#-features)
- [🔧 Installation](#-installation)
- [🚀 Quick Start](#-quick-start)
- [💻 Usage](#-usage)
- [⚙️ Configuration](#-configuration)
- [🌐 API Documentation](#-api-documentation)
- [📚 Tutorials](#-tutorials)
- [🎨 Dashboard](#-dashboard)
- [🔌 Plugin System](#-plugin-system)
- [📊 Output Formats](#-output-formats)
- [🛡️ Security & Best Practices](#-security--best-practices)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🎯 Overview

**SubCandalena (SubHunterX Pro)** adalah tool reconnaissance subdomain tingkat enterprise yang dirancang untuk penetration tester, bug bounty hunter, dan security researcher. Tool ini mengkombinasikan 20+ sumber passive reconnaissance, brute force cerdas, AI-powered mutations, dan analisis vulnerability real-time.

### 🎪 Kenapa SubCandalena?

- **🔍 Comprehensive Discovery**: 20+ sumber passive + brute force intelligence
- **⚡ Lightning Fast**: Multi-threaded dengan asyncio untuk performa maksimal
- **🎨 Beautiful Dashboard**: Web dashboard interaktif dengan visualisasi real-time
- **🤖 AI-Powered**: Mutasi subdomain cerdas dengan pattern learning
- **📊 Rich Reporting**: Export ke JSON, CSV, HTML dengan screenshot
- **🔌 Extensible**: Plugin system untuk custom analyzer
- **🌐 REST API**: Integrasi mudah dengan tool lain
- **💾 Database**: Persistent storage dengan SQLite untuk tracking historical

---

## ✨ Features

### 🔍 Reconnaissance Capabilities

#### 📡 Passive Reconnaissance (20+ Sources)
- **Certificate Transparency**: crt.sh, Censys
- **DNS Services**: DNSDumpster, HackerTarget, ThreatCrowd
- **Search Engines**: Google, Bing, Yahoo dorking
- **Archives**: Wayback Machine, Common Crawl
- **Security Platforms**: VirusTotal, AlienVault OTX, URLScan
- **Code Repositories**: GitHub, GitLab API search
- **Social Media**: Twitter mentions, Pastebin leaks
- **Custom Sources**: 10+ additional proprietary sources

#### ⚡ Active Reconnaissance
- **Intelligent Brute Force**
  - Smart wordlist generation (1k-100k entries)
  - AI-powered permutations & mutations
  - Pattern recognition dari existing subdomains
  - DNS wildcard detection & filtering
  
- **Permutation Engine**
  - Prefix/suffix generation (dev-, staging-, prod-)
  - Number mutations (api1, api2, api-v2)
  - Common patterns (admin, portal, vpn, mail)
  - Custom mutation rules

#### 🔬 Deep Analysis
- **HTTP/HTTPS Probe**: Smart port detection (80, 443, 8080, 8443)
- **Technology Detection**: Framework, CMS, Server identification
- **Screenshot Capture**: Automated visual reconnaissance
- **Response Analysis**: Status codes, redirects, headers
- **SSL/TLS Analysis**: Certificate validation, expiry, issuer
- **Vulnerability Indicators**: Open ports, misconfigurations

### 🎨 User Interface

#### 🖥️ CLI Interface
- Rich terminal output dengan color coding
- Real-time progress bars
- Live statistics updates
- ASCII art banner
- Interactive menus

#### 🌐 Web Dashboard
- **Real-time Monitoring**: Live scan progress
- **Interactive Visualizations**: Charts, graphs, maps
- **Subdomain Explorer**: Filter, search, sort results
- **Screenshot Gallery**: Visual subdomain preview
- **Export Manager**: Download results in multiple formats
- **Scan History**: Track previous scans & compare

#### 🔌 REST API
- **Scan Management**: Start/stop/status endpoints
- **Results Query**: Filter by domain, status, date
- **Export API**: Programmatic data access
- **Webhook Support**: Real-time notifications
- **Authentication**: API key management

### 💾 Data Management

#### 🗄️ Database Features
- **SQLite Storage**: Lightweight persistent database
- **Scan History**: Track all reconnaissance activities
- **Subdomain Tracking**: Monitor changes over time
- **Relationship Mapping**: Parent-child subdomain relations
- **Meta Storage**: Custom fields, tags, notes

#### 📊 Output Formats
- **JSON**: Structured data for automation
- **CSV**: Excel-compatible spreadsheet
- **HTML**: Beautiful web reports with embedded screenshots
- **Markdown**: Documentation-friendly format
- **TXT**: Simple list for piping to other tools

---

## 🔧 Installation

### 📦 Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, Linux, macOS
- **Memory**: 2GB RAM minimum (4GB recommended)
- **Storage**: 500MB free space

### 🚀 Quick Installation

#### Method 1: Clone Repository (Recommended)

```bash
# Clone repository
git clone https://github.com/yourusername/SubCandalena.git
cd SubCandalena

# Install dependencies
pip3 install -r requirements.txt

# Verify installation
python3 main.py --help
```

#### Method 2: Virtual Environment (Best Practice)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tool
python main.py example.com
```

#### Method 3: Docker (Coming Soon)

```bash
docker pull subcandalena/subhunterx:latest
docker run -it subcandalena/subhunterx example.com
```

### 🔍 Dependency Details

```
rich==13.7.1          # Beautiful CLI output
aiohttp==3.9.1        # Async HTTP requests
requests==2.31.0      # HTTP library
fastapi==0.104.1      # REST API framework
uvicorn==0.24.0       # ASGI server
sqlalchemy==2.0.23    # Database ORM
pillow==10.1.0        # Screenshot processing
beautifulsoup4==4.12.2 # HTML parsing
selenium==4.15.2      # Browser automation
plotly==5.17.0        # Data visualization
pyyaml==6.0.1         # Configuration parser
```

---

## 🚀 Quick Start

### ⚡ Basic Usage

```bash
# Simple scan
python main.py example.com

# Quick scan (fast mode)
python main.py example.com --quick

# With dashboard
python main.py example.com --dashboard

# Custom threads
python main.py example.com --threads 100
```

### 📊 Example Output

```
🚀 Starting FULL reconnaissance on example.com

📡 PHASE 1: Passive Reconnaissance
✅ Found 127 passive subdomains

⚡ PHASE 2: Intelligent Brute Force
✅ Found 43 live subdomains

🔬 PHASE 3: Deep Analysis & Vulnerability Assessment
✅ Analyzed 170 subdomains

✅ Scan completed! Found 170 live subdomains

📁 Results saved to: reports/SubCandalena_example_com_20260115_072031.json
```

---

## 💻 Usage

### 🎯 Command-Line Interface

#### Basic Syntax

```bash
python main.py <domain> [options]
```

#### Available Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--dashboard` | `-d` | Open web dashboard after scan | False |
| `--threads` | `-t` | Number of concurrent threads | 50 |
| `--quick` | `-q` | Quick scan mode (100 words, no screenshots) | False |

#### Command Examples

```bash
# Standard reconnaissance
python main.py target.com

# High-speed scan with 100 threads
python main.py target.com --threads 100

# Quick scan for CI/CD integration
python main.py target.com --quick

# Full scan with dashboard
python main.py target.com --dashboard

# Combine multiple options
python main.py target.com --threads 80 --dashboard
```

### 🌐 Web Dashboard

Start the web dashboard:

```bash
# Start dashboard server
python dashboard.py

# Access at: http://localhost:5000
```

Dashboard Features:
- 📊 Real-time scan statistics
- 🔍 Interactive subdomain explorer
- 📸 Screenshot gallery
- 📈 Historical scan comparison
- 💾 Export management

### 🔌 API Server

Start the REST API server:

```bash
# Start API server
python api_server.py

# API available at: http://localhost:8000
```

---

## ⚙️ Configuration

### 📝 Configuration File

Edit `config/config.yaml` to customize behavior:

```yaml
# SubHunterX Pro Configuration

# API Settings
api:
  host: 127.0.0.1
  port: 8000

# Database Settings
database:
  path: ./subhunterx_pro.db

# Scanning Settings
subhunterx:
  threads: 50              # Concurrent threads (10-200)
  timeout: 8               # Request timeout in seconds
  rate_limit: 0.1          # Delay between requests
  screenshot: false        # Enable screenshot capture
  max_screenshots: 20      # Maximum screenshots to capture

# Wordlist Settings
wordlists:
  brute_size: 1000         # Wordlist size (100-100000)
```

### 🎛️ Configuration Options Explained

#### Threads
- **Range**: 10-200
- **Recommended**: 50-100
- **Low (10-30)**: Stealthy, slower
- **Medium (50-80)**: Balanced
- **High (100-200)**: Fast, aggressive

#### Timeout
- **Range**: 3-15 seconds
- **Recommended**: 8
- **Low (3-5)**: Fast but may miss slow servers
- **High (10-15)**: Thorough but slower

#### Brute Size
- **100**: Quick scan (~1 minute)
- **1000**: Standard scan (~5-10 minutes)
- **10000**: Deep scan (~30-60 minutes)
- **100000**: Extreme scan (~2-4 hours)

#### Screenshot Mode
- **false**: Fast, no visual recon
- **true**: Capture webpage screenshots (slower)

---

## 🌐 API Documentation

### 🚀 REST API Endpoints

Base URL: `http://localhost:8000`

#### 🔍 Get Results

```http
GET /api/results?domain=example.com
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "subdomain": "api.example.com",
      "status_code": 200,
      "ip_address": "1.2.3.4",
      "source": "passive",
      "timestamp": "2026-01-15T07:20:31"
    }
  ],
  "count": 127
}
```

#### 🚀 Start Scan

```http
POST /api/scan
Content-Type: application/json

{
  "domain": "example.com"
}
```

**Response:**
```json
{
  "status": "scan_started",
  "domain": "example.com",
  "scan_id": "abc123"
}
```

#### 📊 Scan Status

```http
GET /api/status/{scan_id}
```

**Response:**
```json
{
  "scan_id": "abc123",
  "status": "running",
  "progress": 45,
  "subdomains_found": 78,
  "elapsed_time": "00:05:32"
}
```

### 🐍 Python API Usage

```python
import requests

# Start a scan
response = requests.post('http://localhost:8000/api/scan', 
                         json={'domain': 'example.com'})
scan_id = response.json()['scan_id']

# Check status
status = requests.get(f'http://localhost:8000/api/status/{scan_id}')
print(status.json())

# Get results
results = requests.get('http://localhost:8000/api/results?domain=example.com')
for subdomain in results.json()['data']:
    print(f"{subdomain['subdomain']} - {subdomain['status_code']}")
```

---

## 📚 Tutorials

### 🎯 Tutorial 1: Basic Reconnaissance

**Goal**: Find all subdomains for a target domain

```bash
# Step 1: Run basic scan
python main.py target.com

# Step 2: View results
cat reports/SubCandalena_target_com_*.json

# Step 3: Extract live subdomains
python -c "import json; data=json.load(open('reports/SubCandalena_target_com_*.json')); print('\n'.join([s['subdomain'] for s in data if s['status_code']==200]))"
```

**Expected Output**: List of all discovered subdomains with status codes

---

### 🔥 Tutorial 2: High-Speed Scanning

**Goal**: Scan target as fast as possible

```bash
# Step 1: Configure for speed
python main.py target.com --threads 150 --quick

# Step 2: Results in under 5 minutes
# Quick mode uses:
# - 20 threads only
# - 100 word wordlist
# - No screenshots
# - Basic analysis
```

**Use Cases**: 
- CI/CD pipeline integration
- Quick subdomain validation
- Bug bounty recon phase

---

### 🎨 Tutorial 3: Using the Dashboard

**Goal**: Visual reconnaissance with web interface

```bash
# Step 1: Run scan with dashboard flag
python main.py target.com --dashboard

# Step 2: Dashboard auto-opens at http://localhost:5000

# Step 3: Explore features
# - View real-time progress
# - Filter subdomains by status
# - View screenshots
# - Export custom reports
# - Compare with previous scans
```

**Dashboard Features**:
- 📊 Interactive charts (subdomain distribution, status codes)
- 🔍 Search & filter functionality
- 📸 Screenshot carousel
- 💾 One-click export (JSON/CSV/HTML)
- 📈 Historical trend analysis

---

### 🔌 Tutorial 4: API Integration

**Goal**: Integrate SubCandalena into your workflow

```bash
# Step 1: Start API server
python api_server.py &

# Step 2: Create automation script
```

**automation.py**:
```python
#!/usr/bin/env python3
import requests
import time

API_BASE = "http://localhost:8000"

def scan_domain(domain):
    # Start scan
    response = requests.post(f"{API_BASE}/api/scan", 
                           json={"domain": domain})
    scan_id = response.json()['scan_id']
    
    # Wait for completion
    while True:
        status = requests.get(f"{API_BASE}/api/status/{scan_id}")
        data = status.json()
        
        if data['status'] == 'completed':
            break
            
        print(f"Progress: {data['progress']}% - Found: {data['subdomains_found']}")
        time.sleep(5)
    
    # Get results
    results = requests.get(f"{API_BASE}/api/results?domain={domain}")
    return results.json()['data']

# Usage
targets = ['example.com', 'target.com', 'test.com']
for target in targets:
    print(f"\n🎯 Scanning {target}...")
    subdomains = scan_domain(target)
    print(f"✅ Found {len(subdomains)} subdomains")
```

```bash
# Step 3: Run automation
python automation.py
```

---

### 🔬 Tutorial 5: Advanced Configuration

**Goal**: Optimize for specific scenarios

#### Scenario A: Stealthy Reconnaissance
```yaml
# config/config.yaml
subhunterx:
  threads: 10              # Low thread count
  timeout: 12              # Higher timeout
  rate_limit: 1.0          # 1 second delay between requests
  screenshot: false
wordlists:
  brute_size: 500          # Smaller wordlist
```

```bash
python main.py target.com
# Slow but stealthy, minimal footprint
```

#### Scenario B: Maximum Discovery
```yaml
# config/config.yaml
subhunterx:
  threads: 150             # High concurrency
  timeout: 6               # Lower timeout
  rate_limit: 0.05         # Minimal delay
  screenshot: true         # Capture screenshots
  max_screenshots: 50
wordlists:
  brute_size: 50000        # Large wordlist
```

```bash
python main.py target.com --threads 200
# Aggressive, maximum discovery
```

#### Scenario C: Bug Bounty Hunting
```yaml
# config/config.yaml
subhunterx:
  threads: 80
  timeout: 8
  rate_limit: 0.1
  screenshot: true          # Visual evidence
  max_screenshots: 30
wordlists:
  brute_size: 10000        # Comprehensive wordlist
```

```bash
python main.py target.com --dashboard
# Balanced approach with visual recon
```

---

### 🎯 Tutorial 6: Continuous Monitoring

**Goal**: Track subdomain changes over time

**monitor.sh**:
```bash
#!/bin/bash

DOMAIN="target.com"
INTERVAL=3600  # 1 hour

while true; do
    echo "[$(date)] Starting scan for $DOMAIN"
    
    # Run scan
    python main.py $DOMAIN --quick
    
    # Compare with previous results
    python scripts/compare_scans.py $DOMAIN
    
    # Alert on new subdomains
    python scripts/alert_new.py $DOMAIN
    
    echo "[$(date)] Sleeping for $INTERVAL seconds"
    sleep $INTERVAL
done
```

**compare_scans.py**:
```python
import json
from pathlib import Path
import sys

domain = sys.argv[1]
reports = sorted(Path('reports').glob(f'SubCandalena_{domain.replace(".", "_")}_*.json'))

if len(reports) < 2:
    print("Need at least 2 scans to compare")
    sys.exit(1)

# Load last two scans
with open(reports[-2]) as f:
    old_data = json.load(f)
with open(reports[-1]) as f:
    new_data = json.load(f)

old_subs = {s['subdomain'] for s in old_data}
new_subs = {s['subdomain'] for s in new_data}

# Find differences
added = new_subs - old_subs
removed = old_subs - new_subs

print(f"\n📊 Scan Comparison for {domain}")
print(f"📈 New subdomains: {len(added)}")
for sub in added:
    print(f"  + {sub}")

print(f"\n📉 Removed subdomains: {len(removed)}")
for sub in removed:
    print(f"  - {sub}")
```

---

### 🔌 Tutorial 7: Custom Plugin Development

**Goal**: Extend SubCandalena with custom analyzers

**plugins/custom_analyzer.py**:
```python
"""
Custom Analyzer Plugin Example
Checks for common vulnerabilities in subdomains
"""

class CustomAnalyzer:
    def __init__(self, config):
        self.config = config
        self.vulnerabilities = []
    
    def analyze(self, subdomain, response):
        """
        Analyze subdomain for vulnerabilities
        
        Args:
            subdomain: Subdomain URL
            response: HTTP response object
        
        Returns:
            dict: Analysis results
        """
        results = {
            'subdomain': subdomain,
            'vulnerabilities': []
        }
        
        # Check for sensitive paths
        sensitive_paths = [
            '/.git/config',
            '/.env',
            '/admin',
            '/phpmyadmin',
            '/.aws/credentials'
        ]
        
        for path in sensitive_paths:
            if self.check_path(subdomain + path):
                results['vulnerabilities'].append({
                    'type': 'Exposed Sensitive Path',
                    'path': path,
                    'severity': 'HIGH'
                })
        
        # Check for common misconfigurations
        headers = response.headers
        
        if 'Server' in headers:
            results['server'] = headers['Server']
        
        if 'X-Powered-By' in headers:
            results['vulnerabilities'].append({
                'type': 'Information Disclosure',
                'detail': f"X-Powered-By: {headers['X-Powered-By']}",
                'severity': 'LOW'
            })
        
        return results
    
    def check_path(self, url):
        """Check if path exists"""
        import requests
        try:
            r = requests.get(url, timeout=3, verify=False)
            return r.status_code == 200
        except:
            return False

# Register plugin
def register():
    return CustomAnalyzer
```

**Usage**:
```python
# In main.py or engine.py
from plugins.custom_analyzer import CustomAnalyzer

# Initialize plugin
analyzer = CustomAnalyzer(config)

# Use in scan
for subdomain in subdomains:
    results = analyzer.analyze(subdomain, response)
    if results['vulnerabilities']:
        print(f"🚨 Vulnerabilities found in {subdomain}")
        for vuln in results['vulnerabilities']:
            print(f"  - {vuln['type']}: {vuln.get('detail', 'N/A')}")
```

---

## 🎨 Dashboard

### 🖥️ Dashboard Features

1. **Real-Time Monitoring**
   - Live scan progress
   - Subdomains discovered counter
   - Current phase indicator
   - Elapsed time tracker

2. **Subdomain Explorer**
   - Searchable table
   - Filter by status code
   - Sort by various fields
   - Pagination

3. **Visualizations**
   - Status code distribution (pie chart)
   - Subdomain timeline (line graph)
   - Source breakdown (bar chart)
   - Geolocation map

4. **Screenshot Gallery**
   - Thumbnail grid view
   - Full-size lightbox
   - Download individual screenshots
   - Bulk export

5. **Export Manager**
   - Export to JSON, CSV, HTML
   - Custom field selection
   - Filtered exports
   - Scheduled exports

### 📸 Screenshots

```
Dashboard Preview:
┌─────────────────────────────────────────────────┐
│  SubCandalena Dashboard                         │
├─────────────────────────────────────────────────┤
│  📊 Statistics                                  │
│  Total Subdomains: 237                          │
│  Live: 189 | Down: 48                           │
│  Sources: Passive (145) | Brute (92)            │
├─────────────────────────────────────────────────┤
│  🔍 Search: [_____] 🔽 Filter: All Status      │
├─────────────────────────────────────────────────┤
│  Subdomain              Status  IP           │
│  api.example.com        200     1.2.3.4      │
│  dev.example.com        200     1.2.3.5      │
│  staging.example.com    403     1.2.3.6      │
│  ...                                          │
└─────────────────────────────────────────────────┘
```

---

## 🔌 Plugin System

### 📦 Available Plugins

1. **Custom Analyzer** (`plugins/custom_analyzer.py`)
   - Vulnerability detection
   - Technology fingerprinting
   - Custom checks

2. **Parameter Scanner** (Coming Soon)
   - URL parameter discovery
   - Injection point identification

3. **API Fuzzer** (Coming Soon)
   - API endpoint discovery
   - Parameter fuzzing

### 🛠️ Creating Custom Plugins

See [Tutorial 7: Custom Plugin Development](#-tutorial-7-custom-plugin-development) for detailed guide.

---

## 📊 Output Formats

### 📄 JSON Output

```json
{
  "scan_info": {
    "domain": "example.com",
    "timestamp": "2026-01-15T07:20:31",
    "duration": "00:15:43",
    "total_found": 237
  },
  "subdomains": [
    {
      "subdomain": "api.example.com",
      "ip_address": "1.2.3.4",
      "status_code": 200,
      "title": "API Gateway",
      "server": "nginx",
      "source": "passive",
      "screenshot": "screenshots/api_example_com.png"
    }
  ]
}
```

### 📊 CSV Output

```csv
Subdomain,IP Address,Status Code,Title,Server,Source,Timestamp
api.example.com,1.2.3.4,200,API Gateway,nginx,passive,2026-01-15 07:20:31
dev.example.com,1.2.3.5,200,Dev Environment,Apache,brute,2026-01-15 07:25:18
```

### 🌐 HTML Report

Professional HTML report with:
- Executive summary
- Statistics dashboard
- Subdomain table
- Embedded screenshots
- Export functionality
- Print-friendly layout

### 📝 Text List

```
api.example.com
dev.example.com
staging.example.com
```

---

## 🛡️ Security & Best Practices

### ⚠️ Legal Disclaimer

**IMPORTANT**: Only use SubCandalena on domains you own or have explicit permission to test. Unauthorized scanning may be illegal in your jurisdiction.

### 🔒 Best Practices

1. **Rate Limiting**: Use appropriate rate limits to avoid overwhelming target servers
2. **Threads**: Don't use excessive threads (>200) unless necessary
3. **Scope**: Define clear scope before scanning
4. **Authorization**: Always get written permission
5. **Data Privacy**: Handle discovered data responsibly
6. **Logging**: Keep audit logs of your activities

### 🎯 Ethical Usage

- ✅ Use for authorized penetration testing
- ✅ Use for bug bounty programs (within scope)
- ✅ Use for your own domains
- ❌ Don't scan without permission
- ❌ Don't exploit discovered vulnerabilities
- ❌ Don't share sensitive data publicly

---

## 🤝 Contributing

We welcome contributions! Here's how:

### 🐛 Reporting Bugs

1. Check existing issues
2. Create detailed bug report
3. Include steps to reproduce
4. Attach relevant logs/screenshots

### ✨ Feature Requests

1. Check roadmap & existing requests
2. Describe use case clearly
3. Explain expected behavior
4. Consider implementation complexity

### 🔧 Pull Requests

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### 📝 Code Style

- Follow PEP 8 for Python code
- Use type hints
- Add docstrings
- Write unit tests
- Update documentation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 SubCandalena Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[Full MIT License Text]
```

---

## 🙏 Acknowledgments

- Thanks to all contributors
- Inspired by tools like Sublist3r, Amass, Subfinder
- Built with amazing open-source libraries

---

## 📞 Contact & Support

- **GitHub**: [https://github.com/yourusername/SubCandalena](https://github.com/yourusername/SubCandalena)
- **Issues**: [Report a bug](https://github.com/yourusername/SubCandalena/issues)
- **Email**: support@subcandalena.com
- **Twitter**: [@SubCandalena](https://twitter.com/SubCandalena)

---

## 🗺️ Roadmap

### Version 3.1 (Q1 2026)
- [ ] Docker support
- [ ] Kubernetes scanning
- [ ] Cloud provider integration (AWS, Azure, GCP)
- [ ] Advanced reporting templates

### Version 3.2 (Q2 2026)
- [ ] Machine learning for subdomain prediction
- [ ] Automated vulnerability exploitation
- [ ] Integration with popular security tools
- [ ] Mobile app (iOS/Android)

### Version 4.0 (Q3 2026)
- [ ] Distributed scanning cluster
- [ ] Real-time collaboration
- [ ] Enterprise SaaS platform
- [ ] Advanced AI-powered reconnaissance

---

<div align="center">

### 🌟 Star us on GitHub! 🌟

**Made with ❤️ by Security Researchers, for Security Researchers**

[⬆ Back to Top](#-subcandalena---subhunterx-pro-v30)

</div>

---

## 📖 Additional Resources

### 🎓 Learning Materials

- [Subdomain Enumeration Techniques](docs/techniques.md)
- [DNS Deep Dive](docs/dns-guide.md)
- [Bug Bounty Tips](docs/bugbounty.md)
- [Video Tutorials](https://youtube.com/subcandalena)

### 🔗 Related Tools

- **Sublist3r**: Fast subdomain enumeration
- **Amass**: Network mapping & attack surface discovery
- **Subfinder**: Fast passive subdomain discovery
- **DNSRecon**: DNS enumeration script
- **Knockpy**: Subdomain scanner

### 📚 References

- OWASP Testing Guide
- Bug Bounty Methodology
- DNS RFC Documentation
- Penetration Testing Framework

---

## 🎁 Bonus: Pro Tips

### 💡 Tip 1: Wordlist Optimization
```bash
# Create custom wordlist from discovered subdomains
cat reports/*.json | jq -r '.subdomains[].subdomain' | cut -d'.' -f1 | sort -u > custom_words.txt

# Use custom wordlist
# Edit config.yaml to point to custom_words.txt
```

### 💡 Tip 2: Integration with Other Tools
```bash
# Pipe to nmap for port scanning
python main.py target.com | grep "^[a-z]" | nmap -iL - -oA scan_results

# Pipe to httpx for HTTP probing
python main.py target.com | grep "^[a-z]" | httpx -o live_hosts.txt

# Pipe to nuclei for vulnerability scanning
python main.py target.com | grep "^[a-z]" | nuclei -t cves/ -o vulns.txt
```

### 💡 Tip 3: Automation with Cron
```bash
# Add to crontab for daily scans
0 2 * * * cd /path/to/SubCandalena && python main.py target.com --quick 2>&1 | tee -a logs/daily_scan.log
```

### 💡 Tip 4: Performance Tuning
```bash
# For VPS with limited resources
python main.py target.com --threads 30

# For powerful servers
python main.py target.com --threads 200

# For stealth operations
python main.py target.com --threads 10
```

### 💡 Tip 5: Result Filtering
```python
import json

# Load results
with open('reports/scan.json') as f:
    data = json.load(f)

# Filter only 200 OK
live = [s for s in data['subdomains'] if s['status_code'] == 200]

# Filter by keyword
admin_panels = [s for s in data['subdomains'] if 'admin' in s['subdomain']]

# Export filtered results
with open('filtered.json', 'w') as f:
    json.dump(admin_panels, f, indent=2)
```

---

<div align="center">

**🎯 Happy Hunting! 🎯**

*If you found this tool useful, please consider giving it a ⭐ on GitHub!*

</div>