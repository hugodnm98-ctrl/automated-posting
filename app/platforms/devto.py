import uuid
import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class DevToPlatform(BasePlatform):
    name = "Dev.to"
    API_URL = "https://dev.to/api/articles"

    async def post(self, message: str, cta_url: str) -> PlatformResult:
        if not settings.devto_api_key:
            return self._failure("Missing DEVTO_API_KEY in environment variables")

        try:
            unique_suffix = uuid.uuid4().hex[:6]
            payload = {
                "article": {
                    "title": f"{message[:55]} ({unique_suffix})",
                    "published": True,
                    "body_markdown": f"{message}\n\nLearn more: [{cta_url}]({cta_url})",
                    "tags": ["news", "webdev", "updates"],
                }
            }
            headers = {
                "api-key": settings.devto_api_key,
                "Content-Type": "application/json",
            }
            async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
                resp = await client.post(self.API_URL, json=payload, headers=headers)
                if resp.status_code not in (200, 201):
                    return self._failure(f"HTTP {resp.status_code}: {resp.text[:150]}")
                data = resp.json()
                return self._success(posted_url=data["url"], public_access=True)
        except Exception as exc:
            return self._failure(str(exc))
