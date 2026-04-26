import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client: AsyncIOMotorClient = None
db = None

async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(MONGO_URI)
    db = client.genz
    print("Connected to MongoDB - database: genz")


async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("MongoDB connection closed")


def get_database():
    return db
