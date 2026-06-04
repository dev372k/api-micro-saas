from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from core.config import settings

class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        # Skip docs and health endpoints
        public_paths = [
            "/docs",
            "/openapi.json",
            "/redoc",
            "/health"
        ]

        if request.url.path in public_paths:
            return await call_next(request)

        x_api_key = request.headers.get("X-API-Key")

        if not x_api_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing X-API-Key header"}
            )

        expected_key = settings.X_API_KEY

        if x_api_key != expected_key:
            return JSONResponse(
                status_code=403,
                content={"detail": "Invalid API key"}
            )

        response = await call_next(request)

        return response