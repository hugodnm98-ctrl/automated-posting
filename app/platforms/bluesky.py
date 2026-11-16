from datetime import datetime, timezone
import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class BlueskyPlatform(BasePlatform):
    name = "Bluesky"
    BASE_URL = "https://bsky.social/xrpc"

    async def post(self, message: str, cta_url: str) -> PlatformResult:
        if not settings.bluesky_handle or not settings.bluesky_app_password:
            return self._failure("Missing BLUESKY_HANDLE or BLUESKY_APP_PASSWORD in environment variables")

        try:
            async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
                auth_resp = await client.post(
                    f"{self.BASE_URL}/com.atproto.server.createSession",
                    json={
                        "identifier": settings.bluesky_handle,
                        "password": settings.bluesky_app_password,
                    },
                )
                if auth_resp.status_code != 200:
                    return self._failure("Authentication failed")

                session = auth_resp.json()
                access_jwt = session["accessJwt"]
                did = session["did"]
                handle = session.get("handle", settings.bluesky_handle)

                msg_bytes = message.encode("utf-8")
                url_bytes = cta_url.encode("utf-8")
                byte_start = msg_bytes.find(url_bytes)
                facets = []
                if byte_start != -1:
                    facets.append({
                        "index": {
                            "byteStart": byte_start,
                            "byteEnd": byte_start + len(url_bytes),
                        },
                        "features": [{"": "app.bsky.richtext.facet#link", "uri": cta_url}],
                    })

                record = {
                    "": "app.bsky.feed.post",
                    "text": message,
                    "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                }
                if facets:
                    record["facets"] = facets

                post_resp = await client.post(
                    f"{self.BASE_URL}/com.atproto.repo.createRecord",
                    headers={"Authorization": f"Bearer {access_jwt}"},
                    json={
                        "repo": did,
                        "collection": "app.bsky.feed.post",
                        "record": record,
                    },
                )
                if post_resp.status_code != 200:
                    return self._failure(f"HTTP {post_resp.status_code}: {post_resp.text[:150]}")

                uri = post_resp.json()["uri"]
                rkey = uri.split("/")[-1]
                posted_url = f"https://bsky.app/profile/{handle}/post/{rkey}"
                return self._success(posted_url=posted_url, public_access=True)
        except Exception as exc:
            return self._failure(str(exc))
