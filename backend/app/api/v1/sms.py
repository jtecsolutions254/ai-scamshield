from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.sms import AnalyzeSMSRequest
from app.schemas.common import AnalyzeResponse
from app.services.orchestrator import analyze_text_payload

router = APIRouter()

@router.post("/analyze-sms", response_model=AnalyzeResponse)
def analyze_sms(payload: AnalyzeSMSRequest, db: Session = Depends(get_db)):
    text = payload.text.strip()
    return analyze_text_payload(db=db, kind="sms", raw_text=text, user_visible_text=text)
