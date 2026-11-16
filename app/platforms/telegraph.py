import json
import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class TelegraphPlatform(BasePlatform):
    name = "Telegraph"
    BASE_URL = "https://api.telegra.ph"

    async def _get_or_create_token(self, client: httpx.AsyncClient) -> str:
        if settings.telegraph_access_token:
            return settings.telegraph_access_token

        resp = await client.post(
            f"{self.BASE_URL}/createAccount",
            data={"short_name": "AutoPoster", "author_name": "Automated System"},
        )
        data = resp.json()
        if not data.get("ok"):
            raise RuntimeError(data.get("error", "Failed to create Telegraph account"))
        return data["result"]["access_token"]

    async def post(self, message: str, cta_url: str) -> PlatformResult:
        try:
            async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
                token = await self._get_or_create_token(client)
                content_nodes = [
                    {"tag": "p", "children": [message]},
                    {"tag": "p", "children": [{"tag": "a", "attrs": {"href": cta_url}, "children": [cta_url]}]},
                ]
                resp = await client.post(
                    f"{self.BASE_URL}/createPage",
                    data={
                        "access_token": token,
                        "title": message[:60],
                        "content": json.dumps(content_nodes),
                        "return_content": "false",
                    },
                )
                data = resp.json()
                if not data.get("ok"):
                    return self._failure(data.get("error", "Telegraph API error"))
                return self._success(posted_url=data["result"]["url"], public_access=True)
        except Exception as exc:
            return self._failure(str(exc))
