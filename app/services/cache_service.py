import redis.asyncio as redis
import json
import logging
from typing import Optional

from app.config import get_settings

logger = logging.getLogger(__name__)


class CacheService:
    """Redis cache service for post summaries and recent replies."""

    def __init__(self):
        self.settings = get_settings()
        self._client: Optional[redis.Redis] = None

    async def connect(self) -> None:
        """Establish Redis connection."""
        try:
            self._client = redis.from_url(
                self.settings.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            await self._client.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Caching disabled.")
            self._client = None

    async def disconnect(self) -> None:
        """Close Redis connection."""
        if self._client:
            await self._client.close()
            logger.info("Redis connection closed")

    @property
    def is_connected(self) -> bool:
        """Check if Redis is connected."""
        return self._client is not None

    async def get_post_summary(self, post_id: str) -> Optional[str]:
        """Retrieve cached post summary."""
        if not self._client:
            return None
        try:
            return await self._client.get(f"post_summary:{post_id}")
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    async def set_post_summary(self, post_id: str, summary: str) -> None:
        """Cache post summary."""
        if not self._client:
            return
        try:
            await self._client.setex(
                f"post_summary:{post_id}",
                self.settings.post_summary_ttl,
                summary
            )
        except Exception as e:
            logger.error(f"Cache set error: {e}")

    async def get_recent_replies(self, account_id: str) -> list[str]:
        """Get recent replies for an account to prevent repetition."""
        if not self._client:
            return []
        try:
            data = await self._client.get(f"recent_replies:{account_id}")
            return json.loads(data) if data else []
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return []

    async def add_recent_reply(self, account_id: str, reply: str) -> None:
        """Add a reply to the recent replies list."""
        if not self._client:
            return
        try:
            key = f"recent_replies:{account_id}"
            replies = await self.get_recent_replies(account_id)
            replies.append(reply)
            # Keep only last 50 replies
            replies = replies[-50:]
            await self._client.setex(
                key,
                self.settings.recent_replies_ttl,
                json.dumps(replies)
            )
        except Exception as e:
            logger.error(f"Cache set error: {e}")

    async def health_check(self) -> dict:
        """Check Redis health status."""
        if not self._client:
            return {"redis": "disconnected"}
        try:
            await self._client.ping()
            return {"redis": "healthy"}
        except Exception:
            return {"redis": "unhealthy"}
