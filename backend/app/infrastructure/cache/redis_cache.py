from __future__ import annotations

import json
from typing import Any

from redis.asyncio import Redis


class RedisCache:
    def __init__(self, redis_url: str) -> None:
        self.client = Redis.from_url(redis_url, decode_responses=True)

    async def get(self, key: str) -> dict[str, Any] | None:
        try:
            raw = await self.client.get(key)
            if raw is None:
                return None
            return json.loads(raw)
        except Exception:
            return None

    async def set(self, key: str, payload: dict[str, Any], ttl_seconds: int = 300) -> None:
        try:
            await self.client.set(key, json.dumps(payload), ex=ttl_seconds)
        except Exception:
            return
