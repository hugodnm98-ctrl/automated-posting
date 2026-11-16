import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class GitHubGistPlatform(BasePlatform):
    name = "GitHub Gist"
    API_URL = "https://api.github.com/gists"

    async def post(self, message: str, cta_url: str) -> PlatformResult:
        if not settings.github_token:
            return self._failure("Missing GITHUB_TOKEN in environment variables")

        try:
            payload = {
                "description": message[:100],
                "public": True,
                "files": {
                    "announcement.md": {
                        "content": f"# Announcement\n\n{message}\n"
                    }
                },
            }
            headers = {
                "Authorization": f"Bearer {settings.github_token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
            async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
                resp = await client.post(self.API_URL, json=payload, headers=headers)
                if resp.status_code != 201:
                    return self._failure(f"HTTP {resp.status_code}: {resp.text[:150]}")
                data = resp.json()
                return self._success(posted_url=data["html_url"], public_access=True)
        except Exception as exc:
            return self._failure(str(exc))
