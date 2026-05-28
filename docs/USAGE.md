# SubCandalena Usage Notes

## Core Commands

```bash
python candalena.py example.com
python candalena.py example.com --quick
python candalena.py example.com --threads 100
python candalena.py example.com --dashboard
python api_server.py
```

## Configuration

Edit `config/config.yaml` for scan behavior:

- `subhunterx.threads` / `subhunterx.concurrency`: concurrent scan workers.
- `subhunterx.timeout`: network timeout in seconds.
- `subhunterx.retry`: HTTP retry count.
- `subhunterx.rate_limit`: delay between brute-force checks.
- `subhunterx.resolvers`: optional custom DNS resolvers if `dnspython` is installed.
- `subhunterx.sensitive_paths`: paths checked during risk analysis.
- `passive_sources`: enable or disable passive sources.
- `wordlists.path`: active brute-force wordlist path.

## Outputs

Scans export HTML, JSON, CSV, and TXT files into `reports/`. The HTML report uses a plain table layout with source breakdown, risk reasons, and scan diff sections when previous results exist.

## API

Start the local API:

```bash
python api_server.py
```

Available endpoints:

- `POST /api/scan`
- `GET /api/status/{scan_id}`
- `GET /api/results`
- `GET /api/results/{domain}`
- `GET /api/export/{scan_id}?format=html|json|csv|txt`
