import motor.motor_asyncio
from decouple import config
import asyncio
import json
import nest_asyncio

# Apply the patch to allow nested event loops
nest_asyncio.apply()

MONGO_DETAILS = config("MONGO_DETAILS")  # read environment variable
dbClient = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

# List of databases and collections
databases_and_collections = {
    "backends": ["backends_collection"],
    "functions": ["functions_collection"],
    "jobs": ["jobs_collection"],
    "providers": ["providers_collection"],
    "users": ["users_collection"]
}

# Function to drop existing collections in all databases
async def drop_existing_collections():
    for db_name, collections in databases_and_collections.items():
        database = dbClient[db_name]
        existing_collections = await database.list_collection_names()
        for collection in existing_collections:
            await database.drop_collection(collection)
        print(f"Dropped all collections in database {db_name}")

# Function to initialize databases and collections
async def initialize_database():
    await drop_existing_collections()

    for db_name, collections in databases_and_collections.items():
        database = dbClient[db_name]
        for collection_name in collections:
            await database.create_collection(collection_name)
            print(f"Collection {collection_name} created in database {db_name}")

    print("All collections created successfully in their respective databases")

    # Seed users data into users_collection in the users database
    users_db = dbClient["users"]
    users_collection = users_db["users_collection"]
    
    with open('users.json') as file:
        users_data = json.load(file)
        await users_collection.insert_many(users_data)

    print("Users data seeded successfully into users_collection")

if __name__ == "__main__":
    asyncio.run(initialize_database())