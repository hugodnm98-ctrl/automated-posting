import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class DpastePlatform(BasePlatform):
    name = "dpaste"
    API_URL = "https://dpaste.org/api/"

    async def post(self, message: str, cta_url: str) -> PlatformResult:
        try:
            async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
                resp = await client.post(
                    self.API_URL,
                    data={
                        "content": message,
                        "lexer": "_text",
                        "format": "url",
                        "expires": 2592000,
                    },
                )
                if resp.status_code >= 400:
                    return self._failure(f"HTTP {resp.status_code}: {resp.text[:120]}")
                posted_url = resp.text.strip().strip('"')
                if not posted_url.startswith("http"):
                    return self._failure(f"Unexpected response: {posted_url}")
                return self._success(posted_url=posted_url, public_access=True)
        except Exception as exc:
            return self._failure(str(exc))
