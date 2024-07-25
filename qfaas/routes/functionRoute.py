from fastapi import APIRouter, Body, Depends, Request
from fastapi.encoders import jsonable_encoder
from sympy import re
from qfaas.dependency.auth import get_current_active_user, get_current_user_token
from qfaas.handlers.userHandler import get_role
from qfaas.models.user import UserSchema
from datetime import datetime

from qfaas.handlers.functionHandler import (
    create_function,
    get_functions,
    get_function,
    update_function,
    delete_function,
    invoke_function,
    check_function_permission,
    check_function_permission_invoke,
    function_helper,
    function_helper_get,
    scale_function,
    get_status_function,
)
from qfaas.database.dbFunction import (
    add_function,
    delete_function_db,
    retrieve_function,
)
from qfaas.models.function import (
    ErrorResponseModel,
    ResponseModel,
    ResponseModel,
    FunctionSchema,
    UpdateFunctionModel,
    FunctionInvocationSchema,
    ScaleFunctionModel,
)

router = APIRouter()


@router.post("/", response_description="Function data added into the server")
async def add_function_data(
    function: FunctionSchema = Body(...),
    currentUserUsername: UserSchema = Depends(get_current_active_user),
):
    """Create new function and push to QFaaS

    Args:
    - function (FunctionSchema, optional): Function Schema

    Returns:
    - Function deployed.
    """
    roleCurrentUser = await get_role(currentUserUsername)
    if roleCurrentUser == "admin" or roleCurrentUser == "dev":
        detail, err = create_function(function)
        if err != 0:
            return ErrorResponseModel("An error occurred", 404, detail)
        dataDB = {
            "name": function.template + "-" + function.name,
            "author": currentUserUsername,
            "public": function.public,
        }
        new_function = await add_function(dataDB)
        if new_function:
            return ResponseModel(
                new_function,
                "Function "
                + new_function.get("name")
                + " is pushed successfully to the QFaaS repository and and is being deployed to the QFaaS cluster. Please wait for a few minutes for the deployment to complete.",
            )
        else:
            return ErrorResponseModel(
                "An error occurred",
                404,
                "There was an error when deploying the function. Please contact the QFaaS administrator",
            )
    else:
        return ErrorResponseModel(
            "An error occurred.", 401, "You don't have permissions"
        )


@router.get("/", response_description="Functions retrieved")
async def get_all_functions(
    currentUserUsername: str = Depends(get_current_active_user),
):
    """Get list of all functions

    Returns:
    - All deployed function that the current user has permissions
    """
    functions = get_functions()
    result = []
    for function in functions:
        try:
            checkPermission = await check_function_permission_invoke(
                function["name"], currentUserUsername
            )
            if checkPermission:
                dataDB = await retrieve_function(function["name"])
                if dataDB is None:
                    dataDB = {
                        "name": function["name"],
                        "author": currentUserUsername,
                        "public": True,
                    }
                    await add_function(dataDB)
                    dataDB = await retrieve_function(function["name"])
                status = get_status_function(function["name"])
                function.update(dataDB)
                function.update(status)
                result.append(function_helper(function))
        except:
            pass
    if result != []:
        return ResponseModel(result, "Functions data retrieved successfully")
    return ResponseModel(result, "Empty list returned")


@router.get("/{name}", response_description="Function data retrieved")
async def get_function_data(
    name, currentUserUsername: str = Depends(get_current_active_user)
):
    """Get detail information about a function

    Args:
    - name (_type_): Function name

    Returns:
    - Details about the function
    """
    dataDB = await retrieve_function(name)
    if dataDB is None:
        return ErrorResponseModel(
            "An error occurred.", 404, "Function doesn't exist in database."
        )
    checkPermission = await check_function_permission_invoke(name, currentUserUsername)
    if checkPermission:
        function = get_function(name)
        status = get_status_function(function["name"])
        if function:
            function.update(dataDB)
            function.update(status)
            return ResponseModel(
                function_helper_get(function), "Function data retrieved successfully"
            )
        return ErrorResponseModel("An error occurred.", 404, "Function doesn't exist.")
    else:
        return ErrorResponseModel(
            "An error occurred.", 401, "You don't have permissions"
        )


@router.put("/{name}")
async def update_function_data(
    name,
    req: UpdateFunctionModel = Body(...),
    currentUserUsername: str = Depends(get_current_active_user),
):
    """Update function data

    Args:
    - name (_type_): Function name
    - req (UpdateFunctionModel, optional): Updated function data

    Returns:
    - Function data updated
    """
    dataDB = await retrieve_function(name)
    if dataDB is None:
        return ErrorResponseModel(
            "An error occurred.", 404, "Function doesn't exist in database."
        )
    checkPermission = await check_function_permission(req.name, currentUserUsername)
    if checkPermission:
        function = update_function(req)
        if function:
            return ResponseModel(
                function,
                "Function "
                + name
                + " is updated successfully and is being deployed to the QFaaS cluster. Please wait for a few minutes for the update to take effect.",
            )
        return ErrorResponseModel(
            "An error occurred",
            404,
            "There was an error when updating the function. Please contact the QFaaS administrator",
        )
    else:
        return ErrorResponseModel(
            "An error occurred.", 401, "You don't have permissions"
        )


@router.delete("/{name}", response_description="Function data deleted")
async def delete_function_route(
    name: str, currentUserUsername: str = Depends(get_current_active_user)
):
    """Delete a function

    Args:
    - name (str): function name

    Returns:
    - Function deleted
    """
    dataDB = await retrieve_function(name)
    if dataDB is None:
        return ErrorResponseModel(
            "An error occurred.", 404, "Function doesn't exist in database."
        )
    checkPermission = await check_function_permission(name, currentUserUsername)
    if checkPermission:
        function = delete_function(name)
        if function:
            deleteFunctionDB = await delete_function_db(name)
            return ResponseModel(function, "Function " + name + " is deleted successfully")
        return ErrorResponseModel("An error occurred.", 404, "Function doesn't exist.")
    else:
        return ErrorResponseModel(
            "An error occurred.", 401, "You don't have permissions"
        )


# Invoke function route
@router.post("/{name}", response_description="Invoke function")
async def invoke_function_route(
    name: str,
    request: Request,
    requestData: FunctionInvocationSchema = Body(...),
    currentUserUsername=Depends(get_current_active_user),
):
    """Invoke a function from QFaaS

    Args:
    - name (str): Function name
    - req (FunctionInvocationSchema): Request data

    Returns:
    - Function invocation result (or providerJobId)
    """
    # Check if function exists in database or not
    dataDB = await retrieve_function(name)
    if dataDB is None:
        return ErrorResponseModel(
            "An error occurred", 404, "Function doesn't exist in database."
        )
    # Get current token and forward to function (for backend selection)
    token = request.headers["Authorization"]
    checkPermission = await check_function_permission(name, currentUserUsername)
    if checkPermission:
        try:
            result = await invoke_function(
                name, requestData, currentUserUsername, token
            )
            return ResponseModel(result, "Function invoked successfully")
        except Exception as e:
            return ErrorResponseModel("An error occurred", 500, str(e))
    else:
        return ErrorResponseModel(
            "An error occurred.", 401, "You don't have permissions"
        )


@router.post("/scale/{name}", response_description="Scale function")
async def scale_function_route(
    name: str,
    req: ScaleFunctionModel = Body(...),
    currentUserUsername: str = Depends(get_current_active_user),
):
    dataDB = await retrieve_function(name)
    if dataDB is None:
        return ErrorResponseModel(
            "An error occurred.", 404, "Function doesn't exist in database."
        )
    checkPermission = await check_function_permission(name, currentUserUsername)
    if checkPermission:
        status = scale_function(name, req)
        if status == 200 or status == 202:
            return ResponseModel(req, "Function scale successfully")
        else:
            return ErrorResponseModel(
                "An error occurred.", 404, "Function doesn't exist."
            )
    else:
        return ErrorResponseModel(
            "An error occurred.", 401, "You don't have permissions"
        )
