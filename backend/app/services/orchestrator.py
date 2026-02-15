import hashlib
from uuid import uuid4
from sqlalchemy.orm import Session

from app.models.analysis import Analysis, AnalysisSignal
from app.services.ml_inference import MLInference
from app.services.intel import IntelLayer
from app.services.risk import RiskScorer
from app.services.explain import Explainer
from app.services.cache import CacheStore

ml = MLInference()
intel = IntelLayer()
risk = RiskScorer()
explain = Explainer()
cache = CacheStore()

def _hash_input(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()

def analyze_text_payload(db: Session, kind: str, raw_text: str, user_visible_text: str):
    analysis_id = uuid4().hex
    input_hash = _hash_input(raw_text)

    cache_key = f"text:{kind}:{input_hash}"
    cached = cache.get_json(cache_key)
    if cached:
        ml_result = cached["ml_result"]
        intel_result = cached["intel_result"]
        score = cached["risk_score"]
        level = cached["risk_level"]
        reasons = cached["reasons"]
        actions = cached["recommended_actions"]
    else:
        ml_result = ml.predict_text(raw_text)
        intel_result = intel.inspect_text(user_visible_text)

        score, level = risk.score(
            p_ml=ml_result["prob_phish"],
            h=float(intel_result["heuristic_score"]),
            t=float(intel_result["intel_score"]),
        )

        reasons, actions, _ = explain.explain_text(
            text=user_visible_text,
            ml_prob=ml_result["prob_phish"],
            intel=intel_result,
            level=level
        )

        cache.set_json(
            cache_key,
            {
                "ml_result": ml_result,
                "intel_result": intel_result,
                "risk_score": score,
                "risk_level": level,
                "reasons": reasons,
                "recommended_actions": actions,
            },
            ttl_seconds=6 * 3600,
        )

    a = Analysis(
        id=analysis_id,
        type=kind,
        input_hash=input_hash,
        risk_score=score,
        risk_level=level,
        ml_prob=float(ml_result["prob_phish"]),
        ml_confidence=float(ml_result["confidence"]),
        model_version=ml_result["model_version"],
        raw_excerpt=(user_visible_text[:800] if user_visible_text else None),
    )
    db.add(a)
    db.flush()

    def add_signal(k, v):
        db.add(AnalysisSignal(analysis_id=analysis_id, key=str(k), value=str(v)))

    add_signal("heuristic_score", intel_result["heuristic_score"])
    add_signal("intel_score", intel_result["intel_score"])
    add_signal("urls_found", ",".join(intel_result["urls_found"]))
    add_signal("shortener", intel_result["shortener"])
    add_signal("reputation_hit", intel_result["reputation_hit"])
    if intel_result.get("domain_age_days") is not None:
        add_signal("domain_age_days", intel_result["domain_age_days"])

    db.commit()

    return {
        "type": kind,
        "risk_score": score,
        "risk_level": level,
        "ml": {
            "prob_phish": ml_result["prob_phish"],
            "confidence": ml_result["confidence"],
            "model_version": ml_result["model_version"],
        },
        "intel": {
            "urls_found": intel_result["urls_found"],
            "shortener": intel_result["shortener"],
            "domain_age_days": intel_result.get("domain_age_days"),
            "reputation_hit": intel_result["reputation_hit"],
            "redirects": intel_result.get("redirects", []),
            "notes": intel_result.get("notes", {}),
        },
        "reasons": reasons,
        "recommended_actions": actions,
        "analysis_id": analysis_id,
    }

def analyze_url_payload(db: Session, url: str):
    analysis_id = uuid4().hex
    input_hash = _hash_input(url)

    cache_key = f"url:{input_hash}"
    cached = cache.get_json(cache_key)
    if cached:
        ml_result = cached["ml_result"]
        intel_result = cached["intel_result"]
        score = cached["risk_score"]
        level = cached["risk_level"]
        reasons = cached["reasons"]
        actions = cached["recommended_actions"]
    else:
        ml_result = ml.predict_url(url)
        intel_result = intel.inspect_url(url)

        score, level = risk.score(
            p_ml=ml_result["prob_phish"],
            h=float(intel_result["heuristic_score"]),
            t=float(intel_result["intel_score"]),
        )

        reasons, actions = explain.explain_url(
            url=url,
            ml_prob=ml_result["prob_phish"],
            intel=intel_result,
            level=level
        )

        cache.set_json(
            cache_key,
            {
                "ml_result": ml_result,
                "intel_result": intel_result,
                "risk_score": score,
                "risk_level": level,
                "reasons": reasons,
                "recommended_actions": actions,
            },
            ttl_seconds=6 * 3600,
        )

    a = Analysis(
        id=analysis_id,
        type="url",
        input_hash=input_hash,
        risk_score=score,
        risk_level=level,
        ml_prob=float(ml_result["prob_phish"]),
        ml_confidence=float(ml_result["confidence"]),
        model_version=ml_result["model_version"],
        raw_excerpt=url[:800],
    )
    db.add(a)
    db.flush()

    def add_signal(k, v):
        db.add(AnalysisSignal(analysis_id=analysis_id, key=str(k), value=str(v)))

    add_signal("heuristic_score", intel_result["heuristic_score"])
    add_signal("intel_score", intel_result["intel_score"])
    add_signal("shortener", intel_result["shortener"])
    add_signal("reputation_hit", intel_result["reputation_hit"])
    add_signal("url_length", intel_result["url_length"])
    add_signal("dot_count", intel_result["dot_count"])
    add_signal("has_ip", intel_result["has_ip"])
    if intel_result.get("domain_age_days") is not None:
        add_signal("domain_age_days", intel_result["domain_age_days"])

    db.commit()

    return {
        "type": "url",
        "risk_score": score,
        "risk_level": level,
        "ml": {
            "prob_phish": ml_result["prob_phish"],
            "confidence": ml_result["confidence"],
            "model_version": ml_result["model_version"],
        },
        "intel": {
            "urls_found": [url],
            "shortener": intel_result["shortener"],
            "domain_age_days": intel_result.get("domain_age_days"),
            "reputation_hit": intel_result["reputation_hit"],
            "redirects": intel_result.get("redirects", []),
            "notes": intel_result.get("notes", {}),
        },
        "reasons": reasons,
        "recommended_actions": actions,
        "analysis_id": analysis_id,
    }
