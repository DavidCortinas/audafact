import logging
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from .classifier_models import app as classifier_app
from .config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

main_app = FastAPI(
    title="Audio Intelligence API",
    description="API for audio genre classification and analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc")

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,  # Modify this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        if not rapidapi_proxy_secret or rapidapi_proxy_secret != settings.RAPIDAPI_KEY:
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
