import json
from typing import Any, Optional

import redis

from app.core.config import settings
from app.core.logging import logger


class CacheStore:
    """Best-effort Redis cache.

    If Redis is unavailable, all operations no-op.
    """

    def __init__(self):
        self._client: Optional[redis.Redis] = None

    def _get_client(self) -> Optional[redis.Redis]:
        if self._client is not None:
            return self._client
        try:
            self._client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
            # Ping once to confirm connectivity.
            self._client.ping()
            return self._client
        except Exception as ex:
            logger.info(f"Redis unavailable (cache disabled): {ex}")
            self._client = None
            return None

    def get_json(self, key: str) -> Optional[dict]:
        c = self._get_client()
        if not c:
            return None
        try:
            raw = c.get(key)
            return json.loads(raw) if raw else None
        except Exception:
            return None

    def set_json(self, key: str, value: Any, ttl_seconds: int = 3600) -> None:
        c = self._get_client()
        if not c:
            return
        try:
            c.setex(key, ttl_seconds, json.dumps(value))
        except Exception:
            return
