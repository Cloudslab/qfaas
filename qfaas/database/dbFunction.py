from bson.objectid import ObjectId
from .dbConnect import dbClient

dbFunction = dbClient.functions

function_collection = dbFunction.get_collection("functions_collection")

# Helper format
def function_helper(function) -> dict:
    return {
        "name": str(function["name"]),
        "author": str(function["author"]),
        "public": bool(function["public"]),
    }


# CRUD operations
# Retrieve all functions
async def retrieve_functions():
    functions = []
    async for function in function_collection.find():
        functions.append(function_helper(function))
    return functions


# Add a new function into to the database
async def add_function(function_data: dict) -> dict:
    function = await function_collection.insert_one(function_data)
    new_function = await function_collection.find_one({"_id": function.inserted_id})
    return function_helper(new_function)


# Retrieve a function with a matching ID
async def retrieve_function(name: str) -> dict:
    function = await function_collection.find_one({"name": name})
    if function:
        return function_helper(function)


# Update a function with a matching ID
async def update_function_db(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    function = await function_collection.find_one({"_id": ObjectId(id)})
    if function:
        updated_function = await function_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_function:
            return True
        return False


# Delete a function from the database
async def delete_function_db(name: str):
    function = await function_collection.find_one({"name": name})
    if function:
        await function_collection.delete_one({"name": name})
        return True
