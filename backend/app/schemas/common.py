from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class MLResult(BaseModel):
    prob_phish: float = Field(..., ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)
    model_version: str

class IntelResult(BaseModel):
    urls_found: List[str] = []
    shortener: bool = False
    domain_age_days: Optional[int] = None
    reputation_hit: bool = False
    redirects: List[str] = []
    notes: Dict[str, Any] = {}

class AnalyzeResponse(BaseModel):
    type: str
    risk_score: int = Field(..., ge=0, le=100)
    risk_level: str
    ml: MLResult
    intel: IntelResult
    reasons: List[str]
    recommended_actions: List[str]
    analysis_id: str
