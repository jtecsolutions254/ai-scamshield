from __future__ import annotations
import os
import joblib
from app.core.config import settings
from app.core.logging import logger
from app.utils.text_normalize import normalize_text
from app.utils.url_features import url_to_features

MODEL_VERSION_TEXT = "text-v1"
MODEL_VERSION_URL = "url-v1"

class MLInference:
    def __init__(self):
        self._text_model = None
        self._url_model = None

    def _load_text_model(self):
        if self._text_model is not None:
            return
        path = settings.text_model_path
        if os.path.exists(path):
            self._text_model = joblib.load(path)
            logger.info(f"Loaded text model: {path}")
        else:
            logger.warning(f"Text model not found at {path}. Using heuristic-only fallback.")
            self._text_model = None

    def _load_url_model(self):
        if self._url_model is not None:
            return
        path = settings.url_model_path
        if os.path.exists(path):
            self._url_model = joblib.load(path)
            logger.info(f"Loaded URL model: {path}")
        else:
            logger.warning(f"URL model not found at {path}. Using heuristic-only fallback.")
            self._url_model = None

    def predict_text(self, text: str):
        self._load_text_model()
        clean = normalize_text(text)
        if self._text_model is None:
            return {"prob_phish": 0.50, "confidence": 0.50, "model_version": "fallback"}
        prob = float(self._text_model.predict_proba([clean])[0][1])
        conf = float(max(prob, 1.0 - prob))
        return {"prob_phish": prob, "confidence": conf, "model_version": MODEL_VERSION_TEXT}

    def predict_url(self, url: str):
        self._load_url_model()
        feats = url_to_features(url)
        if self._url_model is None:
            return {"prob_phish": 0.50, "confidence": 0.50, "model_version": "fallback"}
        prob = float(self._url_model.predict_proba([feats])[0][1])
        conf = float(max(prob, 1.0 - prob))
        return {"prob_phish": prob, "confidence": conf, "model_version": MODEL_VERSION_URL}
