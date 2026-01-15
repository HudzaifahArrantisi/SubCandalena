from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, FileResponse
import uvicorn
from ..database.manager import DBManager

app = FastAPI(title="SubHunterX Pro API v3.0")
db = DBManager()

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("frontend/index.html", "r") as f:
        return f.read()

@app.get("/api/results")
async def get_results(domain: str = None):
    results = db.get_results(domain)
    high_risk = [r for r in results if r['risk_score'] > 70]
    return {
        "status": "success",
        "total": len(results),
        "high_risk": len(high_risk),
        "data": results[:100]  # Pagination
    }

@app.get("/api/summary/{domain}")
async def get_summary(domain: str):
    results = db.get_results(domain)
    tech_count = {}
    for r in results:
        for tech in r['tech_stack'].split(','):
            tech_count[tech.strip()] = tech_count.get(tech.strip(), 0) + 1
    
    return {
        "domain": domain,
        "live_subdomains": len(results),
        "avg_risk": sum(r['risk_score'] for r in results) / len(results),
        "top_tech": dict(sorted(tech_count.items(), key=lambda x: x[1], reverse=True)[:5])
    }

def start_api():
    """Start API server"""
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)