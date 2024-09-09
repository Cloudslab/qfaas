import motor.motor_asyncio
from decouple import config
import asyncio
import json

MONGO_DETAILS = config("MONGO_DETAILS")  # read environment variable
dbClient = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

# Create new Database called qfaas
database = dbClient.qfaas

# drop all collections if they exist
async def drop_exising_collections():
    existingCollections = await database.list_collection_names()
    for collection in existingCollections:
        await database.drop_collection(collection)

# Create all required collections
async def intilize_database():
    await drop_exising_collections()
    collectionNames = ["backends", "functions", "jobs", "providers", "users"]

    for collectionName in collectionNames:
        await database.create_collection(collectionName)
        print(f"Collection {collectionName} created")

    print("All collections created successfully in the database qfaas")

    # seed users data
    users = database["users"]
    with open('users.json') as file:
        usersData = json.load(file)
        await users.insert_many(usersData)

        print("Users data seeded successfully")

if __name__ == "__main__":
    asyncio.run(intilize_database())
