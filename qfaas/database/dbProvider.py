from bson.objectid import ObjectId
from .dbConnect import dbClient

dbProvider = dbClient.providers

provider_collection = dbProvider.get_collection("providers_collection")

# Helper format
def provider_helper(provider) -> dict:
    return {
        "username": str(provider["username"]),
        "providerName": str(provider["providerName"]),
        "providerToken": str(provider["providerToken"]),
        "additionalInfo": dict(provider["additionalInfo"]),
    }

# CRUD operations
# Retrieve all providers
async def retrieve_providers(username: str):
    providers = []
    async for provider in provider_collection.find({"username": username}):
        providers.append(provider_helper(provider))
    return providers

# Add a new provider into to the database
async def add_provider(provider_data: dict) -> dict:
    provider = await provider_collection.insert_one(provider_data)
    new_provider = await provider_collection.find_one({"_id": provider.inserted_id})
    return provider_helper(new_provider)


# Retrieve a provider with a matching ID
async def retrieve_provider(username: str, providerName: str) -> dict:
    provider = await provider_collection.find_one({"username": username, 'providerName': providerName})
    if provider:
        return provider_helper(provider)

# Update a provider with a matching ID
async def update_provider(username: str, providerName: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    provider = await provider_collection.find_one({"username": username, 'providerName': providerName})
    if provider:
        updated_provider = await provider_collection.update_one(
            {"username": username, "providerName": providerName}, {"$set": data}
        )
        if updated_provider:
            updatedProvider = await provider_collection.find_one({"username": username, 'providerName': providerName})
            return provider_helper(updatedProvider)
        return False


# Delete a provider from the database
async def delete_provider(username: str, providerName: str):
    provider = await provider_collection.find_one({"username": username, "providerName": providerName})
    if provider:
        await provider_collection.delete_one({"username": username, "providerName": providerName})
        return True
