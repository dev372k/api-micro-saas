from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routes.user_route import user_router
from routes.subscription_route import subscription_router
from routes.payment_route import payment_router
from routes.webhook_route import webhook_router
from core.config import settings
from core.logging import logger

app = FastAPI(title=settings.APP_NAME)

app.include_router(user_router)
app.include_router(subscription_router)
app.include_router(payment_router)
app.include_router(webhook_router)

@app.get("/")
def root():
    logger.info("Root endpoint called")

    return JSONResponse(status_code=200, content={
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    })
