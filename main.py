from fastapi import FastAPI
from routes.routes import router
from core.config import settings
from core.logging import logger

app = FastAPI(title=settings.APP_NAME)

app.include_router(router)

@app.get("/")
def root():
    logger.info("Root endpoint called")

    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }