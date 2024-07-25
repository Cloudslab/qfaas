import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config

MONGO_DETAILS = config("MONGO_DETAILS")  # read environment variable
dbClient = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)