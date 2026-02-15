from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.url import AnalyzeURLRequest
from app.schemas.common import AnalyzeResponse
from app.services.orchestrator import analyze_url_payload

router = APIRouter()

@router.post("/analyze-url", response_model=AnalyzeResponse)
def analyze_url(payload: AnalyzeURLRequest, db: Session = Depends(get_db)):
    return analyze_url_payload(db=db, url=payload.url)
