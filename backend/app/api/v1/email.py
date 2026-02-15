from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.email import AnalyzeEmailRequest
from app.schemas.common import AnalyzeResponse
from app.services.orchestrator import analyze_text_payload

router = APIRouter()

@router.post("/analyze-email", response_model=AnalyzeResponse)
def analyze_email(payload: AnalyzeEmailRequest, db: Session = Depends(get_db)):
    text = "\n".join([
        f"Subject: {payload.subject or ''}",
        f"From: {payload.sender or ''}",
        payload.headers_raw or "",
        payload.body
    ]).strip()
    return analyze_text_payload(db=db, kind="email", raw_text=text, user_visible_text=payload.body)
