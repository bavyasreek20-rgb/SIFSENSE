from pydantic import BaseModel, Field
from typing import List, Optional


class AnalyzeRequest(BaseModel):
    report_text: str = Field(..., min_length=5, max_length=10000)
    site: str = Field(default="Unspecified site", max_length=200)
    activity: str = Field(default="Unspecified activity", max_length=200)
    report_type: str = Field(default="Near Miss", max_length=100)


class PrecursorEvidence(BaseModel):
    phrase: str
    category: str
    severity_weight: int
    matched_text: str


class AnalyzeResponse(BaseModel):
    id: int
    report_text: str
    site: str
    activity: str
    report_type: str
    classification: str
    severity_score: int
    evidence: List[PrecursorEvidence]
    life_saving_rules: List[str]
    recommendation: str
    disclaimer: str


class ReportRecord(AnalyzeResponse):
    created_at: str


class SummaryResponse(BaseModel):
    total_reports: int
    sif_potential: int
    non_sif_potential: int
    average_severity_score: float
