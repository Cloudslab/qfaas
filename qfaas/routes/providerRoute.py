from enum import Enum
from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from sympy import false
from qfaas.dependency.auth import get_current_active_user
from qfaas.database.dbProvider import (
    add_provider,
    update_provider,
    delete_provider,
    retrieve_provider,
    retrieve_providers,
)
from qfaas.models.provider import (
    ErrorResponseModel,
    ResponseModel,
    CreateProviderModel,
    UpdateProviderModel,
)
from qfaas.utils.logger import logger
from qfaas.providers.ibmq import get_IBMQ_hubs
from qfaas.providers.braketsw import initialize_SWProvider

from qfaas.routes.backendRoute import fetch_backend

router = APIRouter()


class ProviderName(str, Enum):
    ibmq = ("ibmq",)
    braketsw = "braket-sw"


@router.post("/", response_description="Provider data added into the database")
async def add_provider_data(
    provider: CreateProviderModel = Body(...),
    currentUserUsername: str = Depends(get_current_active_user),
):
    """Add new Provider data to the database

    Args:
    - provider (CreateProviderModel, optional): Provider data as example format (provider name must be "ibmq" or "braket-sw")

    Returns:
    - New provider data added
    """
    provider = jsonable_encoder(provider)
    # Check duplicate provider
    providerName = provider["providerName"]
    checkProvider = await retrieve_provider(currentUserUsername, providerName)
    if checkProvider:
        return ErrorResponseModel(
            "Provider " + providerName + " already exists",
            400,
            "Please update its information or add other provider information.",
        )
    provider["username"] = currentUserUsername
    # Verify provider info
    if providerName == "ibmq":
        logger.info("Verifying IBMQ Token")
        hubs = get_IBMQ_hubs(provider["providerToken"])
        defaultHub = provider["additionalInfo"]["defaultHub"]
        if hubs:
            provider["additionalInfo"]["hub"] = hubs
            if defaultHub:
                if defaultHub not in hubs:
                    provider["additionalInfo"]["defaultHub"] = hubs[0]
            else:
                provider["additionalInfo"]["defaultHub"] = hubs[0]
        else:
            return ErrorResponseModel(
                "Invalid IBMQ API Token",
                400,
                "Please check again and provide a valid IBMQ with access to IBM Quantum Backends",
            )
    elif providerName == "braket-sw":
        pass
    else:
        return ErrorResponseModel(
            "Invalid Provider Name",
            400,
            "Please check again and provide a valid provider name. Current supported providers are ibmq and braket-sw",
        )

    new_provider = await add_provider(provider)
    await fetch_backend(providerName, currentUserUsername)
    return ResponseModel(
        new_provider, "New provider added successfully. All available backend fetched"
    )


@router.get("/", response_description="Providers retrieved")
async def get_providers(currentUserUsername: str = Depends(get_current_active_user)):
    """Get all providers of current user

    Returns:
    - All available providers retrieved
    """
    providers = await retrieve_providers(currentUserUsername)
    if providers:
        return ResponseModel(providers, "Providers data retrieved successfully")
    return ResponseModel(providers, "Empty list returned")


@router.get("/{providerName}", response_description="Provider data retrieved")
async def get_provider_data(
    providerName: ProviderName,
    currentUserUsername: str = Depends(get_current_active_user),
):
    """Get specific provider information

    Args:
    - providerName (str): Provider name (ibmq, braket-sw)

    Returns:
    - Provider data retrieved
    """
    provider = await retrieve_provider(currentUserUsername, providerName)
    if provider:
        return ResponseModel(provider, "Provider data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Provider doesn't exist.")


@router.put("/{providerName}")
async def update_provider_data(
    providerName: str,
    req: UpdateProviderModel = Body(...),
    currentUserUsername: str = Depends(get_current_active_user),
):
    """Update Provider Information (also update backend information from provider)

    Args:
    - providerName (str): Provider name
    - req (UpdateProviderModel, optional): Update data

    Returns:
    - New information of provider and new backend information from updated provider updated
    """
    # Verifying API Token
    if providerName == "ibmq":
        logger.info("Verifying IBMQ Token")
        hubs = get_IBMQ_hubs(req.providerToken)
        if hubs:
            req.additionalInfo["hub"] = hubs
            defaultHub = req.additionalInfo["defaultHub"]
            if defaultHub:
                if defaultHub not in hubs:
                    req.additionalInfo["defaultHub"] = hubs[0]
            else:
                req.additionalInfo["defaultHub"] = hubs[0]
        else:
            return ErrorResponseModel(
                "Invalid IBMQ API Token",
                400,
                "Please check again and provide a valid IBMQ with access to IBM Quantum Backends",
            )
    elif providerName == "braket-sw":
        try:
            swUser = req.additionalInfo["swUser"]
            swConnection = initialize_SWProvider(swUser, req.providerToken)
            if swConnection is False:
                return ErrorResponseModel(
                    "Invalid swUser or Strangeworks API Token",
                    400,
                    "Please check again and provide a valid swUser with API Token to access Strangeworks Quantum",
                )
        except:
            return ErrorResponseModel(
                "Invalid swUser or Strangeworks API Token",
                400,
                "Please check again and provide a valid swUser with API Token to access Strangeworks Quantum",
            )
    else:
        return ErrorResponseModel(
            "Invalid Provider Name",
            400,
            "Please check again and provide a valid provider name. Current supported providers are ibmq and braket-sw",
        )
    # Update to database
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_provider = await update_provider(currentUserUsername, providerName, req)

    if updated_provider:
        if providerName == "ibmq":
            # Fetching new backend information
            logger.info("Fetching new IBMQ backend information")
            await fetch_backend("ibmq", currentUserUsername)
        return ResponseModel(
            updated_provider,
            "Provider information ({}) updated successfully".format(providerName),
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the provider data.",
    )


@router.delete(
    "/{providerName}", response_description="Provider data deleted from the database"
)
async def delete_provider_data(
    providerName: str, currentUserUsername: str = Depends(get_current_active_user)
):
    """Delete Provider data

    Args:
    - providerName (str): Provider name (ibmq, braket-sw)

    Returns:
    - Provider data deleted from the database
    """
    deleted_provider = await delete_provider(currentUserUsername, providerName)
    if deleted_provider:
        return ResponseModel(
            "Provider with ID: {} removed".format(id), "Provider deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Provider with id {0} doesn't exist".format(id)
    )
