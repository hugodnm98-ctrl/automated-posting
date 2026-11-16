import re
from typing import List, Optional
from urllib.parse import urlparse
from pydantic import BaseModel, field_validator


URL_REGEX = re.compile(r"https?://[^\s<>\"']+|www\.[^\s<>\"']+", re.IGNORECASE)


class PostingRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Message cannot be empty.")

        if len(cleaned) > 200:
            raise ValueError(
                f"Message exceeds the 200-character limit (current length: {len(cleaned)})."
            )

        urls = URL_REGEX.findall(cleaned)
        if len(urls) == 0:
            raise ValueError("Message must include exactly one CTA link (0 links found).")
        if len(urls) > 1:
            raise ValueError(
                f"Message must include exactly one CTA link ({len(urls)} links found)."
            )

        url = urls[0]
        if not url.lower().startswith(("http://", "https://")):
            raise ValueError(f"CTA link must start with http:// or https:// (got: {url}).")

        parsed = urlparse(url)
        if not parsed.netloc or "." not in parsed.netloc:
            raise ValueError(f"Invalid CTA URL format: {url}")

        return cleaned

    def extract_url(self) -> str:
        return URL_REGEX.findall(self.message)[0]


class PlatformResult(BaseModel):
    platform: str
    status: str
    posted_url: Optional[str] = None
    public_access: bool = False
    date: Optional[str] = None
    time: Optional[str] = None
    error: Optional[str] = None


class PostingResponse(BaseModel):
    success: bool
    results: List[PlatformResult]
