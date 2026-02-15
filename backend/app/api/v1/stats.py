from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.db import get_db
from app.models.analysis import Analysis

router = APIRouter()

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(func.count(Analysis.id)).scalar() or 0
    by_type = dict(db.query(Analysis.type, func.count(Analysis.id)).group_by(Analysis.type).all())
    by_level = dict(db.query(Analysis.risk_level, func.count(Analysis.id)).group_by(Analysis.risk_level).all())

    recent = (
        db.query(Analysis)
        .order_by(Analysis.created_at.desc())
        .limit(10)
        .all()
    )

    return {
        "total": total,
        "by_type": by_type,
        "by_level": by_level,
        "recent": [
            {
                "id": a.id,
                "type": a.type,
                "risk_score": a.risk_score,
                "risk_level": a.risk_level,
                "created_at": a.created_at.isoformat() + "Z",
                "excerpt": (a.raw_excerpt or "")[:220],
            }
            for a in recent
        ]
    }
