import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader

from config import get_settings, Settings
from app.models import (
    ReplyRequest,
    ReplyResponse,
    SummarizeRequest,
    SummarizeResponse,
    HealthResponse,
)
from app.services.claude_service import ClaudeService
from app.services.cache_service import CacheService
from app.services.reply_generator import ReplyGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# API Key Security
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """Verify the API key from request header."""
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing API key. Include 'X-API-Key' header."
        )

    settings = get_settings()
    valid_keys = [k.strip() for k in settings.api_keys.split(",") if k.strip()]

    if not valid_keys:
        # If no API keys configured, allow all requests (dev mode)
        logger.warning("No API keys configured - running in development mode")
        return "dev_mode"

    if api_key not in valid_keys:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )

    return api_key


# Global service instances
cache_service: CacheService = None
claude_service: ClaudeService = None
reply_generator: ReplyGenerator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown."""
    global cache_service, claude_service, reply_generator

    # Startup
    logger.info("Starting Roborder AI Reply Service...")

    cache_service = CacheService()
    await cache_service.connect()

    claude_service = ClaudeService()
    reply_generator = ReplyGenerator(claude_service, cache_service)

    logger.info("Service started successfully")
    yield

    # Shutdown
    logger.info("Shutting down...")
    await cache_service.disconnect()
    logger.info("Service stopped")


app = FastAPI(
    title="Roborder AI Reply Service",
    description="Multimodal AI-powered Instagram comment reply system with optional Seller Knowledge Base",
    version="2.0.0",
    lifespan=lifespan,
)

# Configure CORS
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    """Check service health status."""
    cache_status = await cache_service.health_check() if cache_service else {"redis": "not initialized"}
    return HealthResponse(
        status="healthy",
        version="2.0.0",
        services=cache_status
    )


@app.post("/api/v1/generate-reply", response_model=ReplyResponse)
async def generate_reply(
    request: ReplyRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Generate a human-like reply to an Instagram comment.

    Uses Claude Vision to analyze post images and generate contextual,
    culturally-appropriate replies in French, Arabic, or English.

    When seller_context is provided, generates highly accurate replies
    with exact prices, shipping info, and product details.

    Requires X-API-Key header for authentication.
    """
    try:
        response = await reply_generator.generate(request)
        has_context = request.seller_context is not None
        logger.info(
            f"Generated reply for post {request.post_id}: "
            f"intents={response.detected_intents}, confidence={response.confidence:.2f}, "
            f"context={'full' if has_context else 'fallback'}"
        )
        return response
    except Exception as e:
        logger.error(f"Error generating reply: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/summarize-post", response_model=SummarizeResponse)
async def summarize_post(
    request: SummarizeRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Generate and cache a summary of an Instagram post.

    This summary is used to generate contextual replies to comments.
    The summary is cached to reduce API calls for subsequent comments
    on the same post.

    Requires X-API-Key header for authentication.
    """
    try:
        # Check cache first
        cached_summary = await cache_service.get_post_summary(request.post_id)
        if cached_summary:
            logger.info(f"Cache hit for post {request.post_id}")
            return SummarizeResponse(
                post_id=request.post_id,
                summary=cached_summary,
                cached=True
            )

        # Generate new summary
        summary = await claude_service.summarize_post(
            caption=request.caption,
            image_urls=request.image_urls
        )

        # Cache the summary
        await cache_service.set_post_summary(request.post_id, summary)
        logger.info(f"Generated and cached summary for post {request.post_id}")

        return SummarizeResponse(
            post_id=request.post_id,
            summary=summary,
            cached=False
        )
    except Exception as e:
        logger.error(f"Error summarizing post: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"status": "running"}


