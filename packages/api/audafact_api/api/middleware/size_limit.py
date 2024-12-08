from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import logging

logger = logging.getLogger(__name__)


class MaxSizeLimitMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: ASGIApp, max_upload_size: int):
        super().__init__(app)
        self.max_upload_size = max_upload_size
        logger.info(
            f"MaxSizeLimitMiddleware initialized with max size: {max_upload_size}"
        )

    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("Content-Length")
        logger.info(f"MaxSizeLimitMiddleware: Content-Length header: {content_length}")

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
                    detail=f"File size {content_length} exceeds allowed limit {self.max_upload_size}",
                )

        return await call_next(request)
