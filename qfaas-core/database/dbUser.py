from bson.objectid import ObjectId
from .dbConnect import dbClient
from qfaas.utils.auth import get_password_hash, verify_password

dbUser = dbClient.users

user_collection = dbUser.get_collection("users_collection")

# Helper format


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": str(user["username"]),
        "displayName": str(user["displayName"]),
        "role": str(user["role"]),
        "hashedPassword": str(user["hashedPassword"]),
        "currentToken": str(user["currentToken"]),
    }


def user_helper_min(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": str(user["username"]),
        "displayName": str(user["displayName"]),
        "role": str(user["role"]),
    }


# CRUD operations
# Retrieve all users


async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


async def retrieve_users_min():
    users = []
    async for user in user_collection.find():
        users.append(user_helper_min(user))
    return users


# Add a new user into to the database
async def add_user(user_data: dict) -> dict:
    hashedPassword = get_password_hash(user_data["password"])
    user_data.pop("password")
    user_data = {
        **user_data,
        "hashedPassword": hashedPassword,
        "disabled": False,
        "role": "member",
        "displayName": "New QFaaS user",
        "currentToken": "",
    }
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper_min(new_user)


# Retrieve a user with a matching username
async def retrieve_user(username: str) -> dict:
    user = await user_collection.find_one({"username": username})
    if user:
        return user_helper(user)


# Retrieve a user with a matching username
async def retrieve_user_token(username: str) -> str:
    user = await user_collection.find_one({"username": username})
    if user:
        return str(user["currentToken"])


# Update a user with a matching ID
async def update_user(username: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"username": username})
    if user and data["currentPassword"] is not None:
        verifyPass = verify_password(data["currentPassword"], user["hashedPassword"])
        if verifyPass is True:
            data.pop("currentPassword")
            if (
                data["newPassword"] is not None
                and data["newPasswordConfirm"] is not None
            ):
                if data["newPassword"] != data["newPasswordConfirm"]:
                    return False
                else:
                    newPasswordHash = get_password_hash(data["newPassword"])
                    data["hashedPassword"] = newPasswordHash
            data.pop("newPassword")
            data.pop("newPasswordConfirm")
            updated_user = await user_collection.update_one(
                {"username": username}, {"$set": data}
            )
            if updated_user:
                return True
            return False


# Update a user with a matching ID
async def update_user_token(username: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"username": username})
    if user:
        updated_user = await user_collection.update_one(
            {"username": username}, {"$set": data}
        )
        if updated_user:
            return True
        return False


# Delete a user from the database
async def delete_user(username: str):
    user = await user_collection.find_one({"username": username})
    if user:
        await user_collection.delete_one({"username": username})
        return True
