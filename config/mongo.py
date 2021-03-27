from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from config.base import settings


db_client = AsyncIOMotorClient(settings.MONGO_DATABASE_URI)
engine = AIOEngine(motor_client=db_client, database=settings.MONGO_DB)

