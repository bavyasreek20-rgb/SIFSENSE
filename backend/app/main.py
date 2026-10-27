from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from . import database
from .analyzer import analyze_report
from .schemas import AnalyzeRequest, AnalyzeResponse, ReportRecord, SummaryResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield


app = FastAPI(
    title="SIFSense API",
    description="Prototype API for explainable SIF precursor triage in safety reports.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"service": "SIFSense API", "status": "running", "version": "0.1.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    result = analyze_report(request.report_text)
    payload = {
        "report_text": request.report_text,
        "site": request.site,
        "activity": request.activity,
        "report_type": request.report_type,
        **result,
    }
    report_id = database.save_report(payload)
    return {"id": report_id, **payload}


@app.get("/reports", response_model=List[ReportRecord])
def reports(limit: int = Query(default=50, ge=1, le=200)):
    return database.list_reports(limit)


@app.get("/reports/{report_id}", response_model=ReportRecord)
def report_detail(report_id: int):
    item = database.get_report(report_id)
    if not item:
        raise HTTPException(status_code=404, detail="Report not found")
    return item


@app.get("/summary", response_model=SummaryResponse)
def summary():
    return database.get_summary()
