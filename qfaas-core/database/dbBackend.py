from bson.objectid import ObjectId
from .dbConnect import dbClient
from qfaas.utils.logger import logger

dbBackend = dbClient.backends

backend_collection = dbBackend.get_collection("backends_collection")

# Helper format
def backend_helper(backend) -> dict:
    return {
        "id": str(backend["_id"]),
        "name": str(backend["name"]),
        "provider": str(backend["provider"]),
        "type": str(backend["type"]),
        "qubit": str(backend["qubit"]),
        "user": str(backend["user"]),
        "active": str(backend["active"]),
        "sdk": str(backend["sdk"]),
        "backendInfo": dict(backend["backendInfo"]),
    }


# CRUD operations
async def get_backends_from_db(
    user: str,
    provider: str = "",
    name: str = "",
    sdk: str = "",
    bkType: str = "",
):
    if user:
        query = {"user": user}
        if provider:
            query["provider"] = provider
        if name:
            query["name"] = name
        if sdk:
            query["sdk"] = sdk
        if bkType:
            query["type"] = bkType
    else:
        # If user is null, do nothing
        return False
    backends = backend_collection.find(query)
    backendList = []
    async for bk in backends:
        backendList.append(backend_helper(bk))
    return backendList


# Add a new backend into to the database
async def add_backend(backend_data: dict) -> dict:
    backend = await backend_collection.insert_one(backend_data)
    new_backend = await backend_collection.find_one({"_id": backend.inserted_id})
    return backend_helper(new_backend)


# Add many backend into to the database
async def add_many_backends(backend_data: list):
    # Convert backend schema to dict
    backendDict = []
    for backend in backend_data:
        if type(backend) == dict:
            backendDict.append(backend)
        else:
            backendDict.append(backend.__dict__)
    bki = await backend_collection.insert_many(backendDict)
    ids = bki.inserted_ids
    backends = []
    async for bk in backend_collection.find({"_id": {"$in": ids}}):
        backends.append(backend_helper(bk))
    return backends


# Retrieve a backend with a matching ID
async def retrieve_backend(id: str) -> dict:
    backend = await backend_collection.find_one({"_id": ObjectId(id)})
    if backend:
        return backend_helper(backend)


# Retrieve a backend by name
async def retrieve_backend_by_name(name: str, user: str) -> dict:
    backend = await backend_collection.find_one({"name": name, "user": user})
    if backend:
        return backend_helper(backend)
    else:
        return None


# Update a backend with a matching ID
async def update_backend(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    backend = await backend_collection.find_one({"_id": ObjectId(id)})
    if backend:
        updated_backend = await backend_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_backend:
            newBackend = await backend_collection.find_one({"_id": ObjectId(id)})
            return backend_helper(newBackend)
        return False


# Delete a backend from the database
async def delete_backend(id: str):
    backend = await backend_collection.find_one({"_id": ObjectId(id)})
    if backend:
        await backend_collection.delete_one({"_id": ObjectId(id)})
        return True


# Delete all backends of a user
async def delete_many_backends(user: str, provider: str = ""):
    if user:
        if provider:
            query = {"user": user, "provider": provider}
        else:
            query = {"user": user}
    else:
        # If user is null, do nothing
        return False
    # logger.info(query)
    backends = backend_collection.find(query)
    if backends:
        backend_collection.delete_many(query)
        return True
