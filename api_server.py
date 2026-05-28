import asyncio
import uuid
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from subhunterx.core.engine import SubHunterXEngine
from subhunterx.database.manager import DBManager
from subhunterx.utils.helpers import is_valid_domain, load_config
from subhunterx.utils.visualizer import Visualizer

app = FastAPI(title="SubCandalena API")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

db = DBManager()
scan_jobs = {}


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    with open("frontend/index.html", encoding="utf-8") as f:
        return f.read()


@app.post("/api/scan")
async def start_scan(domain: Optional[str] = None, payload: dict = Body(default=None)):
    target = domain or (payload or {}).get("domain")
    if not target or not is_valid_domain(target):
        raise HTTPException(status_code=400, detail="Valid domain is required")

    scan_id = uuid.uuid4().hex
    scan_jobs[scan_id] = {"scan_id": scan_id, "domain": target, "status": "queued", "progress": 0, "error": None}
    asyncio.create_task(_run_scan(scan_id, target))
    return scan_jobs[scan_id]


@app.get("/api/status/{scan_id}")
async def scan_status(scan_id: str):
    if scan_id not in scan_jobs:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan_jobs[scan_id]


@app.get("/api/results")
async def get_results(domain: Optional[str] = None):
    return db.get_results(domain)


@app.get("/api/results/{domain}")
async def get_domain_results(domain: str):
    return db.get_results(domain)


@app.get("/api/export/{scan_id}")
async def export_scan(scan_id: str, format: str = "html"):
    job = scan_jobs.get(scan_id)
    if not job:
        raise HTTPException(status_code=404, detail="Scan not found")
    results = db.get_all_subdomains(job["domain"])
    viz = Visualizer(results, job["domain"])
    if format == "json":
        path = viz.export_json()
    elif format == "csv":
        path = viz.export_csv()
    elif format == "txt":
        path = viz.export_txt()
    else:
        path = viz.create_dashboard()
    if not path or not Path(path).exists():
        raise HTTPException(status_code=500, detail="Export failed")
    return FileResponse(path)


async def _run_scan(scan_id: str, domain: str):
    try:
        scan_jobs[scan_id].update({"status": "running", "progress": 10})
        config = load_config()
        engine = SubHunterXEngine(domain, config)
        results = await engine.full_scan()
        scan_jobs[scan_id].update(
            {
                "status": "completed",
                "progress": 100,
                "count": len(results),
                "engine_scan_id": engine.scan_id,
            }
        )
    except Exception as exc:
        scan_jobs[scan_id].update({"status": "failed", "error": str(exc), "progress": 100})


if __name__ == "__main__":
    config = load_config()
    uvicorn.run(app, host=config["api"]["host"], port=int(config["api"]["port"]))
