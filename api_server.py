from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from subhunterx.database.manager import DBManager

app = FastAPI(title="SubHunterX Pro API")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

db = DBManager()

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    with open("frontend/index.html") as f:
        return f.read()

@app.get("/api/results")
async def get_results(domain: str = None):
    results = db.get_results(domain)
    return {"status": "success", "data": results, "count": len(results)}

@app.post("/api/scan")
async def start_scan(domain: str):
    # Trigger scan
    return {"status": "scan_started", "domain": domain}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)