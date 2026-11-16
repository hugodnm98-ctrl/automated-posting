from abc import ABC, abstractmethod
from datetime import datetime, timezone
from app.schemas import PlatformResult


class BasePlatform(ABC):
    name: str = "Base Platform"

    @abstractmethod
    async def post(self, message: str, cta_url: str) -> PlatformResult:
        raise NotImplementedError

    def _success(self, posted_url: str, public_access: bool = True) -> PlatformResult:
        now = datetime.now(timezone.utc)
        return PlatformResult(
            platform=self.name,
            status="success",
            posted_url=posted_url,
            public_access=public_access,
            date=now.strftime("%Y-%m-%d"),
            time=now.strftime("%H:%M:%S"),
            error=None,
        )

    def _failure(self, error_message: str) -> PlatformResult:
        return PlatformResult(
            platform=self.name,
            status="failed",
            posted_url=None,
            public_access=False,
            date=None,
            time=None,
            error=error_message,
        )
