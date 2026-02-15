from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(String, primary_key=True)
    type = Column(String, nullable=False)  # email|sms|url
    input_hash = Column(String, nullable=False, index=True)

    risk_score = Column(Integer, nullable=False)
    risk_level = Column(String, nullable=False)
    ml_prob = Column(Float, nullable=True)
    ml_confidence = Column(Float, nullable=True)
    model_version = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    raw_excerpt = Column(Text, nullable=True)

    signals = relationship("AnalysisSignal", back_populates="analysis", cascade="all, delete-orphan")

class AnalysisSignal(Base):
    __tablename__ = "analysis_signals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    analysis_id = Column(String, ForeignKey("analyses.id"), nullable=False, index=True)

    key = Column(String, nullable=False)
    value = Column(String, nullable=False)

    analysis = relationship("Analysis", back_populates="signals")
