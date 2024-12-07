import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from .classifier_models import app as classifier_app
from .config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"Loaded RapidAPI Proxy Secret: {settings.RAPIDAPI_PROXY_SECRET}")


class MaxSizeLimitMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: ASGIApp, max_upload_size: int):
        super().__init__(app)
        self.max_upload_size = max_upload_size
        logger.info(
            f"MaxSizeLimitMiddleware initialized with max size: {max_upload_size}"
        )

    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("Content-Length")
        logger.info(
            f"MaxSizeLimitMiddleware: Content-Length header: {content_length}")

        if content_length:
            content_length = int(content_length)
            logger.info(
                f"MaxSizeLimitMiddleware: Checking size {content_length} against limit {self.max_upload_size}"
            )
            if content_length > self.max_upload_size:
                logger.warning(
                    f"File size {content_length} exceeds limit {self.max_upload_size}"
                )
                raise HTTPException(
                    status_code=413,
                    detail=
                    f"File size {content_length} exceeds allowed limit {self.max_upload_size}"
                )

        return await call_next(request)


main_app = FastAPI(
    title="Audio Intelligence API",
    description="API for audio genre classification and analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc")

main_app.add_middleware(MaxSizeLimitMiddleware,
                        max_upload_size=10 * 1024 * 1024)

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,  # Modify this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@main_app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log detailed request information
    headers = dict(request.headers)
    logger.info(f"Incoming request headers: {headers}")
    logger.info(f"Incoming request: {request.method} {request.url}")

    # Log content length if present
    if 'content-length' in headers:
        logger.info(f"Content Length: {headers['content-length']}")

    # Log RapidAPI specific headers
    logger.info(
        f"RapidAPI Proxy Secret: {headers.get('x-rapidapi-proxy-secret')}")
    logger.info(f"RapidAPI Key: {headers.get('x-rapidapi-key')}")

    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


@main_app.get("/health")
async def health_check():
    return {"status": "healthy"}


@main_app.get("/")
async def root():
    return {
        "message": "Welcome to the Audio Intelligence API",
        "description": "Audio analysis and genre classification services",
        "documentation": {
            "general_docs": "/docs",
            "detailed_docs": "/redoc",
            "custom_docs": "/api-docs"
        },
        "access":
        "Subscribe to our API at https://rapidapi.com/DavidCortinas/api/audafact-music-intelligence",
        "status": {
            "health_check": "/health",
            "metrics": "/metrics"
        }
    }


@main_app.get("/metrics")
async def metrics():
    return {"uptime": "...", "request_count": "...", "error_count": "..."}


main_app.mount("/api/", classifier_app)


@main_app.middleware("http")
async def check_subscription_tier(request: Request, call_next):
    # Get subscription tier from RapidAPI header
    subscription = request.headers.get("X-RapidAPI-Subscription", "").lower()

    # Block file endpoint for Basic plan
    if subscription == "BASIC" and "/genres/file" in request.url.path:
        raise HTTPException(
            status_code=403,
            detail=
            "File upload endpoint is only available for Pro, Ultra, and Mega plans"
        )

    return await call_next(request)


@main_app.middleware("http")
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
            request.url.path.startswith(prefix) for prefix in doc_prefixes):
        return await call_next(request)

    if settings.require_auth:
        rapidapi_proxy_secret = request.headers.get("X-RapidAPI-Proxy-Secret")
        if not rapidapi_proxy_secret or rapidapi_proxy_secret != settings.RAPIDAPI_PROXY_SECRET:
            raise HTTPException(status_code=403, detail="Not authorized")

    return await call_next(request)


@main_app.get("/api-docs", include_in_schema=False)
async def custom_docs():
    return HTMLResponse("""
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
    """)


@main_app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error: {exc.detail}")
    return {"error": exc.detail}, exc.status_code


@main_app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled error: {str(exc)}", exc_info=True)
    return {"error": "Internal server error"}, 500


if __name__ == "__main__":
    import uvicorn

    port = int(settings.PORT)
    logger.info(f"Starting server on port: {port}")

    uvicorn.run("main:main_app",
                host="0.0.0.0",
                port=port,
                reload=settings.ENV == "development")
