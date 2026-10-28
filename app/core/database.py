from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional

from app.core.config import settings


class DatabaseManager:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None


db_manager = DatabaseManager()


async def connect_to_mongo():
    """Initializes the MongoDB Atlas async client connection."""
    db_manager.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db_manager.db = db_manager.client[settings.MONGODB_DB_NAME]
    print("✅ Connected to MongoDB Atlas successfully.")


async def close_mongo_connection():
    """Closes the MongoDB Atlas async client connection."""
    if db_manager.client:
        db_manager.client.close()
        print("✅ Closed MongoDB Atlas connection.")


def get_database() -> AsyncIOMotorDatabase:
    """Returns active MongoDB database instance."""
    if db_manager.db is None:
        raise RuntimeError("Database connection has not been initialized.")
    return db_manager.db