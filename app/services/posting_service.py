import asyncio
from typing import List
from app.platforms.base import BasePlatform
from app.platforms.bluesky import BlueskyPlatform
from app.platforms.devto import DevToPlatform
from app.platforms.dpaste import DpastePlatform
from app.platforms.github_gist import GitHubGistPlatform
from app.platforms.telegraph import TelegraphPlatform
from app.schemas import PlatformResult


class PostingService:
    def __init__(self, platforms: List[BasePlatform] | None = None):
        self.platforms = platforms or [
            TelegraphPlatform(),
            DpastePlatform(),
            DevToPlatform(),
            GitHubGistPlatform(),
            BlueskyPlatform(),
        ]

    async def publish_all(self, message: str, cta_url: str) -> List[PlatformResult]:
        tasks = [platform.post(message=message, cta_url=cta_url) for platform in self.platforms]
        raw_results = await asyncio.gather(*tasks, return_exceptions=True)

        results: List[PlatformResult] = []
        for platform, item in zip(self.platforms, raw_results):
            if isinstance(item, Exception):
                results.append(
                    PlatformResult(
                        platform=platform.name,
                        status="failed",
                        posted_url=None,
                        public_access=False,
                        date=None,
                        time=None,
                        error=str(item),
                    )
                )
            else:
                results.append(item)
        return results
