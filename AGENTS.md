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