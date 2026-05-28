# 🎯 SubCandalena (SubHunterX Pro v3.0)

SubCandalena is an enterprise-grade subdomain reconnaissance and intelligence suite designed for security researchers and penetration testers. It combines passive discovery, intelligent brute force, and deep vulnerability analysis.

## 🏗 Project Overview

- **Purpose:** Comprehensive subdomain discovery and analysis.
- **Main Technologies:**
  - **Language:** Python 3.8+
  - **Async:** `asyncio`, `aiohttp` for high-performance scanning.
  - **CLI:** `rich` for beautiful terminal output.
  - **API:** `FastAPI` & `uvicorn` for RESTful integration.
  - **Database:** `SQLAlchemy` with SQLite for persistent tracking.
  - **Visualization:** `plotly` and a web dashboard.
- **Key Modules:**
  - `subhunterx.core.engine`: Orchestrates the 3-phase scanning process.
  - `subhunterx.core.passive`: Aggregates results from 20+ passive sources.
  - `subhunterx.core.brute`: Performs multi-threaded brute force with AI-powered mutations.
  - `subhunterx.core.analyzer`: Deep HTTP/SSL analysis and screenshot capture.

## 🚀 Building and Running

### Prerequisites
- Python 3.8 or higher.
- `pip` for dependency management.

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# (Optional) Run one-click setup to initialize directory structure
python setup.py
```

### Running the Tool
- **CLI Scan:** `python candalena.py example.com`
  - `--dashboard`: Open web dashboard after scan.
  - `--threads <n>`: Set number of concurrent threads.
  - `--quick`: Fast scan with limited wordlist and no screenshots.
- **Web Dashboard:** `python dashboard.py` (Default: http://localhost:5000)
- **REST API Server:** `python api_server.py` (Default: http://localhost:8000)

## ⚙️ Development Conventions

- **Code Style:** Follows PEP 8 guidelines.
- **Project Structure:**
  - `subhunterx/`: Core logic and modules.
  - `config/`: YAML-based configuration management.
  - `data/`: Storage for wordlists and screenshots.
  - `reports/`: Generated JSON, CSV, and HTML reports.
  - `frontend/`: Web dashboard assets.
- **Configuration:** Managed via `config/config.yaml`. The `load_config` helper in `subhunterx/utils/helpers.py` handles merging defaults.
- **Database:** Uses SQLite (`subhunterx_pro.db`). Models are defined in `subhunterx/database/models.py`.

## 🛠 Key Files

- `candalena.py`: Primary CLI entry point.
- `api_server.py`: FastAPI-based REST server.
- `dashboard.py`: Dashboard launcher.
- `setup.py`: Environment and directory initialization.
- `requirements.txt`: Project dependencies.
- `config/config.yaml`: Central configuration for scans, API, and database.
