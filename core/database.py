import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

client = AsyncIOMotorClient(
    settings.MONGODB_URI,
    tls=True,
    tlsCAFile=certifi.where()
)