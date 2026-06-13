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

        rapidapi_proxy_secret_key = request.headers.get("X-RapidAPI-Proxy-Secret")

        if not rapidapi_proxy_secret_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing X-RapidAPI-Proxy-Secret"}
            )

        expected_key = settings.RAPIDAPI_PROXY_SECRET_KEY

        if rapidapi_proxy_secret_key != expected_key:
            return JSONResponse(
                status_code=403,
                content={"detail": "Invalid API key"}
            )

        response = await call_next(request)

        return response