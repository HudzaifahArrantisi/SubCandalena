# Repository Guidelines

## Project Overview

SubCandalena is a Python-based subdomain reconnaissance and intelligence tool.

Primary goals:
- Fast reconnaissance
- Modular architecture
- Reusable scanning modules
- Safe and maintainable code
- Production-quality CLI and API behavior

---

## AI Agent Role

Act as a Senior Python Security Engineer and Recon Automation Engineer.

Before making any change:
1. Read repository structure first
2. Understand dependencies
3. Analyze current implementation
4. Preserve existing architecture
5. Prefer minimal safe changes

Never make assumptions.

---

## Repository Structure & Module Organization

Main entry points:
- `candalena.py` → CLI entrypoint
- `api_server.py` → FastAPI dashboard/API
- `dashboard.py` → dashboard launcher

Core package:
- `subhunterx/core/` → orchestration & discovery engine
- `subhunterx/modules/` → feature scanners
- `subhunterx/database/` → SQLite persistence
- `subhunterx/api/` → API helpers
- `subhunterx/utils/` → helpers, wordlists, visualization

Frontend:
- `frontend/` → dashboard static assets

Configuration:
- `config/config.yaml`

Wordlists:
- `data/wordlists/`

Extensions:
- `plugins/`

Generated outputs:
- reports
- screenshots
- local databases

Never commit generated outputs unless explicitly requested.

---

## Critical Engineering Rules

### DO

- Follow existing architecture
- Reuse existing logic whenever possible
- Prefer extending modules over rewriting
- Keep CLI logic thin
- Put reusable logic inside package modules
- Use strong error handling
- Add logging when useful
- Prefer type hints
- Add docstrings to public methods
- Keep changes modular

### DO NOT

- Do NOT rewrite working architecture
- Do NOT delete imports without verification
- Do NOT create duplicate logic
- Do NOT rename files without reason
- Do NOT break backward compatibility
- Do NOT introduce unnecessary abstractions
- Do NOT overengineer

Always minimize blast radius of changes.

---

## Coding Style & Naming Conventions

Follow:
- PEP 8
- 4-space indentation
- snake_case → modules/functions/files
- PascalCase → classes

Use:
- clear naming
- type hints
- concise functions
- modular structure

Avoid:
- giant functions
- nested complexity
- duplicated logic

---

## Debugging Workflow

When debugging:

1. Find root cause first
2. Read traceback/logs
3. Inspect affected module
4. Verify config assumptions
5. Verify database/network behavior
6. Propose minimal safe fix
7. Explain why bug happened

Never guess.

---

## Testing Rules

Before finalizing:

Minimum validation:

```bash
python candalena.py example.com --quick
python api_server.py
```

Run unit tests:

```bash
python -m unittest tests/test_core_logic.py
```

Tests cover: domain validation, risk scoring, takeover detection, snapshot diffing.

---

## Key Commands

```bash
# Setup
pip install -r requirements.txt
python setup.py

# Full scan
python candalena.py example.com

# Quick scan (100 words, 20 threads, no screenshots)
python candalena.py example.com --quick

# Scan with exports
python candalena.py example.com --export all

# Directory scan on live hosts
python candalena.py example.com -d

# API server (port 8000)
python api_server.py

# Dashboard (port 5000)
python dashboard.py
```

---

## Architecture Notes

- **3-Phase Pipeline**: passive recon (`core/passive.py`) → brute force (`core/brute.py`) → deep analysis (`core/analyzer.py`)
- **Async/Sync Mix**: passive + brute phases use `asyncio` + `aiohttp`; analysis uses `ThreadPoolExecutor` + `requests`
- **Windows Quirk**: `subhunterx/utils/asyncio_compat.py` sets `SelectorEventLoop` policy for SSL on Windows
- **Config Loading**: `helpers.py:load_config()` deep-merges YAML defaults; `config/config.py` is a standalone duplicate — prefer `helpers.py`
- **Database**: SQLAlchemy ORM with SQLite (`subhunterx_pro.db`); auto-migration via `_ensure_subdomain_columns()`
- **Plugin System**: Protocol-based in `subhunterx/plugins.py`; example at `plugins/custom_analyzer.py`

---

## Known Gotchas

- Empty module stubs exist: `modules/paramscan.py`, `permutation.py`, `bruteforce.py` (0 lines) — planned but unimplemented
- No linter/formatter config enforced — follow PEP 8 manually
- No CI/CD pipelines — validation is manual
- `subhunterx_pro.db` is a runtime artifact — do not commit
- README/docs use Indonesian + English mix
