from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas import PostingRequest, PostingResponse
from app.services.posting_service import PostingService

app = FastAPI(
    title="Automated Multi-Platform Posting System",
    description="REST API to validate and broadcast messages with a CTA link across multiple platforms.",
    version="1.0.0",
)

posting_service = PostingService()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [err.get("msg", "Invalid input") for err in exc.errors()]
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "detail": errors,
        },
    )


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/posting", response_model=PostingResponse)
async def create_posting(payload: PostingRequest):
    try:
        cta_url = payload.extract_url()
        results = await posting_service.publish_all(
            message=payload.message,
            cta_url=cta_url,
        )
        overall_success = any(r.status == "success" for r in results)
        return PostingResponse(success=overall_success, results=results)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
