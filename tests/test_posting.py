from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from app.main import app, posting_service
from app.schemas import PlatformResult

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_validation_message_too_long():
    long_msg = ("A" * 190) + " https://example.com"
    response = client.post("/posting", json={"message": long_msg})
    assert response.status_code == 422


def test_validation_no_url():
    response = client.post("/posting", json={"message": "Check out our latest platform without link."})
    assert response.status_code == 422


def test_validation_multiple_urls():
    msg = "Visit https://example.com and also https://another.com today."
    response = client.post("/posting", json={"message": msg})
    assert response.status_code == 422


def test_posting_partial_failure_resilience(monkeypatch):
    mock_results = [
        PlatformResult(
            platform="Telegraph",
            status="success",
            posted_url="https://telegra.ph/test-123",
            public_access=True,
            date="2026-11-16",
            time="17:00:00",
            error=None,
        ),
        PlatformResult(
            platform="Bluesky",
            status="failed",
            posted_url=None,
            public_access=False,
            date=None,
            time=None,
            error="Authentication failed",
        ),
    ]
    monkeypatch.setattr(posting_service, "publish_all", AsyncMock(return_value=mock_results))

    response = client.post(
        "/posting",
        json={"message": "Check out our latest business platform. https://example.com"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["results"]) == 2
    assert data["results"][0]["status"] == "success"
    assert data["results"][1]["status"] == "failed"
