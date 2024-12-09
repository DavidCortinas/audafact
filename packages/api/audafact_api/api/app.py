import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from .middleware.size_limit import MaxSizeLimitMiddleware
from .routes import genres, mood_themes, tags
from ..core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Music Intelligence API",
    description="API for music genre classification and analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(MaxSizeLimitMiddleware, max_upload_size=10 * 1024 * 1024)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,  # Modify this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log detailed request information
    headers = dict(request.headers)
    logger.info(f"Incoming request headers: {headers}")
    logger.info(f"Incoming request: {request.method} {request.url}")

    # Log content length if present
    if "content-length" in headers:
        logger.info(f"Content Length: {headers['content-length']}")

    # Log RapidAPI specific headers
    logger.info(f"RapidAPI Proxy Secret: {headers.get('x-rapidapi-proxy-secret')}")
    logger.info(f"RapidAPI Key: {headers.get('x-rapidapi-key')}")

    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Audio Intelligence API",
        "description": "Audio analysis and genre classification services",
        "documentation": {
            "general_docs": "/docs",
            "detailed_docs": "/redoc",
            "custom_docs": "/api-docs",
        },
        "access": "Subscribe to our API at https://rapidapi.com/DavidCortinas/api/audafact-music-intelligence",
        "status": {"health_check": "/health", "metrics": "/metrics"},
    }


@app.get("/metrics")
async def metrics():
    return {"uptime": "...", "request_count": "...", "error_count": "..."}


app.include_router(genres.router, prefix="/api")
app.include_router(mood_themes.router, prefix="/api")
app.include_router(tags.router, prefix="/api")


@app.middleware("http")
async def check_subscription_tier(request: Request, call_next):
    # Get subscription tier from RapidAPI header
    subscription = request.headers.get("X-RapidAPI-Subscription", "").lower()

    # Block file endpoint for Basic plan
    if subscription == "BASIC" and "/genres/file" in request.url.path:
        raise HTTPException(
            status_code=403,
            detail="File upload endpoint is only available for Pro, Ultra, and Mega plans",
        )

    return await call_next(request)


@app.middleware("http")
async def verify_rapidapi_proxy(request, call_next):
    # Only allow public access to main app docs and basic endpoints
    public_paths = {
        # Basic endpoints
        "/health",
        "/metrics",
        "/",
        # Main app documentation (showing only general info)
        "/docs",
        "/redoc",
        "/api-docs",
        "/openapi.json",
        "/docs/oauth2-redirect",
    }

    # Check if the path starts with any of these prefixes
    doc_prefixes = ("/docs/", "/redoc/")
    if request.url.path in public_paths or any(
        request.url.path.startswith(prefix) for prefix in doc_prefixes
    ):
        return await call_next(request)

    if settings.require_auth:
        rapidapi_proxy_secret = request.headers.get("X-RapidAPI-Proxy-Secret")
        if (
            not rapidapi_proxy_secret
            or rapidapi_proxy_secret != settings.RAPIDAPI_PROXY_SECRET
        ):
            raise HTTPException(status_code=403, detail="Not authorized")

    return await call_next(request)


@app.get("/api-docs", include_in_schema=False)
async def custom_docs():
    return HTMLResponse(
        """
    <html>
        <head>
            <title>Audio Intelligence API Documentation</title>
        </head>
        <body>
            <h1>Audio Intelligence API Documentation</h1>
            <p>This API provides audio analysis and genre classification services.</p>

            <h2>Documentation</h2>
            <ul>
                <li>General API information at <a href="/docs">/docs</a></li>
                <li>Detailed documentation at <a href="/redoc">/redoc</a></li>
            </ul>

            <h2>Using the API</h2>
            <p>To access and test the API endpoints:</p>
            <ol>
                <li>Visit our <a href="https://rapidapi.com/DavidCortinas/api/audafact-music-intelligence">RapidAPI marketplace page</a></li>
                <li>Subscribe to get your API key</li>
                <li>Use the key to make requests to our endpoints</li>
            </ol>

            <h2>API Status</h2>
            <ul>
                <li>Check API health at <a href="/health">/health</a></li>
                <li>View metrics at <a href="/metrics">/metrics</a></li>
            </ul>
        </body>
    </html>
    """
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error: {exc.detail}")
    # Fix: Don't return tuple, return JSONResponse
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled error: {str(exc)}", exc_info=True)
    # Fix: Don't return tuple, return JSONResponse
    return JSONResponse(status_code=500, content={"error": "Internal server error"})
