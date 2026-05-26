from fastapi import FastAPI, Request
from routes.routes import router
from core.config import settings
from core.logging import logger
from middlewares.auth import RapidAPIAuthMiddleware

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(RapidAPIAuthMiddleware)
app.include_router(router)

@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }

@app.get("/health")
def health():
    logger.info("Health endpoint called")
    return {
        "status": "ok"
    }

@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()

    logger.info("Webhook endpoint called")
    logger.info(f"Webhook payload: {payload}")

    return {
        "message": "Webhook received"
    }
