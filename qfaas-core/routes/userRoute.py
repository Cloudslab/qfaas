from fastapi import APIRouter, Body, Depends
from qfaas.dependency.auth import get_current_active_user
from qfaas.handlers.userHandler import get_role
from qfaas.database.dbUser import (
    update_user,
    delete_user,
    retrieve_user,
    retrieve_users_min,
)
from qfaas.models.user import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UpdateUserModel,
)

router = APIRouter()


@router.get("/all", response_description="All users retrieved")
async def get_users(currentUserUsername: str = Depends(get_current_active_user)):
    """Get all users (for Administrator only)

    Returns:
    - List of all users
    """
    roleCurrentUser = await get_role(currentUserUsername)
    if roleCurrentUser == "admin":
        users = await retrieve_users_min()
        if users:
            return ResponseModel(users, "All users data retrieved successfully")
        else:
            ResponseModel(users, "Empty list returned")
    else:
        return ErrorResponseModel(
            "An error occurred.", 401, "You don't have permissions"
        )


@router.get("/", response_description="User data retrieved")
async def get_user_data(currentUserUsername: str = Depends(get_current_active_user)):
    """Get detailed information of current user.

    Returns:
    - Details of current user
    """
    user = await retrieve_user(currentUserUsername)
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")


@router.put("/")
async def update_user_data(
    req: UpdateUserModel = Body(...),
    currentUserUsername: str = Depends(get_current_active_user),
):
    """Update user information (display name)

    Args:
    - req (UpdateUserModel, optional): Updated User Model (displayName)

    Returns:
    - User information updated
    """
    req = {k: v for k, v in req.dict().items()}
    updated_user = await update_user(currentUserUsername, req)
    if updated_user:
        return ResponseModel(
            "User with name {} update is successful".format(currentUserUsername),
            "User name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )


@router.delete("/", response_description="User data deleted from the database")
async def delete_user_by_username(
    username: str, currentUserUsername: str = Depends(get_current_active_user)
):
    """Delete user by username (for Administrator only)

    Args:
    - username (str): username

    Returns:
    - User data deleted from the database
    """
    roleCurrentUser = await get_role(currentUserUsername)
    if roleCurrentUser == "admin":
        deleted_user = await delete_user(username)
        if deleted_user:
            return ResponseModel(
                "User {} removed".format(username), "User deleted successfully"
            )
        return ErrorResponseModel(
            "An error occurred", 404, "User {} doesn't exist".format(username)
        )
    else:
        return ErrorResponseModel(
            "An error occurred.", 401, "You don't have permissions"
        )
