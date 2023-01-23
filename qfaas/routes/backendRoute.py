from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from qfaas.utils.logger import logger
from enum import Enum

from qfaas.database.dbBackend import (
    add_backend,
    add_many_backends,
    update_backend,
    delete_backend,
    delete_many_backends,
    retrieve_backend,
    retrieve_backend_by_name,
    get_backends_from_db,
)
from qfaas.models.backend import (
    ErrorResponseModel,
    ResponseModel,
    BackendSchema,
    UpdateBackendModel,
    BackendRequestSchema,
)
from qfaas.models.user import UserSchema
from qfaas.database.dbUser import retrieve_user

# Get IBMQ Backends
from qfaas.providers.ibmq import get_ibmq_backends, get_ibmq_default_hub
from qfaas.providers.braketsw import get_braketsw_backends
from qfaas.dependency.auth import get_current_active_user
from qfaas.handlers.backendHandler import select_backend

router = APIRouter()

# Add new internal backend to database (external backend will be queried directly from external provider)
class ProviderName(str, Enum):
    all = "all"
    qfaas = "qfaas"
    ibmq = "ibmq"
    braketsw = "braket-sw"


# Backend Selection route
@router.post("/select", response_description="Backend Selection completed")
async def backend_selection_route(
    beReq: BackendRequestSchema, currentUsername: str = Depends(get_current_active_user)
):
    """Verify and select an approriate backend based on user request

    Args:
    - **BackendRequestSchema**:
      - _sdk_: Type of SDK or language, i.e., "qiskit", "qsharp", "cirq" or "braket"
      - _provider_: Provider name, i.e., "ibmq" (IBM Quantum), "braket-sw" (Amazon Braket via Strangeworks) or "qfaas" (Local provider)
      - _rQubit_ (Optional, default = 1): Required qubit, e.g, 10
      - _type_ (Optional): Type of Backend, i.e., "simulator" or "qpu". Remove type to select any available
      - _autoSelect_ (Optional, default = False): Automatically selecr at least busy backend
      - _backendName_ (Optional): Backend name in case user prefer to select backend manually, e.g., "ibm_hanoi", "ibmq_qasm_simulator"

    Returns:
    - Backend information and Provider Token (use for establish connection to that backend)
    """
    if beReq.sdk in ["qiskit", "qsharp", "cirq", "braket"]:
        backend = await select_backend(beReq, currentUsername)
    else:
        return False
    if backend:
        return ResponseModel(backend, "Backend selected and validated successfully.")
    else:
        return ErrorResponseModel(
            "Backend not found",
            404,
            "No such backend found. Please check your request parameters (and default hub name in case of using IBM Quantum).",
        )


# Add backend
@router.post("/", response_description="Backend data added into the database")
async def add_backend_data(backend: BackendSchema = Body(...)):
    """
    Create a new Internal backend (at K8s cluster) with these information:
    - **name**: Backend name, e.g., "cirq_simulator"
    - **provider**: Provider name, internal provider is "qfaas"
    - **type**: quantum computer ("qpu") or "simulator",
    - **qubit**: number of maximum supported qubit,
    - **user**: username have access to the backend,
    - **backendInfo**: Extra information about the backend
    """
    backend = jsonable_encoder(backend)  # Encode data to JSON for DB
    new_backend = await add_backend(backend)
    return ResponseModel(new_backend, "Backend added successfully.")


# Get all backends
@router.get("/", response_description="Backends retrieved")
async def get_backends(
    provider: ProviderName, currentUsername: str = Depends(get_current_active_user)
) -> list:
    """Get backends list from local Database. (To retrieve updated information from external provider, use the **fetch()** method)

    **Args**:
    - **provider** (ProviderName): Provider name (ibmq, braket-sw, qfaas). "all" to retrieve all backends from all providers.

    Returns:
    - **backendList** (list): Backend list from local database.
    """
    if provider == "all":
        backendList = await get_backends_from_db(currentUsername)
        return ResponseModel(
            backendList,
            str(len(backendList))
            + " backends of all providers are retrieved successfully.",
        )
    elif provider in ["qfaas", "ibmq", "braket-sw"]:
        backendList = await get_backends_from_db(currentUsername, provider)
    else:
        return ErrorResponseModel(
            "An error occurred.",
            404,
            "Provider ("
            + str(provider)
            + ") doesn't exist or invalid. Please try again.",
        )
    return ResponseModel(
        backendList,
        str(len(backendList))
        + " backends of provider "
        + provider
        + " are retrieved successfully (from local database).",
    )


@router.get(
    "/fetch", response_description="Fetch backend information from Quantum Provider"
)
async def fetch_backend(
    provider: ProviderName, currentUsername: str = Depends(get_current_active_user)
) -> list:
    """
    Fetch new backend information from Quantum Providers and synchonize with local database.

    **Args**:
    - **provider** (str, optional): Provider name (ibmq, braket-sw or all). Defaults to "all" providers.

    **Returns**:
    - **backendList** (list): Backend list from selected providers
    """
    currentUser = await retrieve_user(currentUsername)
    if provider == "all":
        hub = await get_ibmq_default_hub(currentUsername)
        ibmqBackend = await get_ibmq_backends(currentUser, hub)
        braketSwBackend = await get_braketsw_backends(currentUser)
        internalBackend = await get_backends_from_db(currentUsername, "qfaas")
        backendList = ibmqBackend + braketSwBackend + internalBackend
        provider = ""
    elif provider == "ibmq":
        hub = await get_ibmq_default_hub(currentUsername)
        backendList = await get_ibmq_backends(currentUser, hub)
    elif provider == "braket-sw":
        backendList = await get_braketsw_backends(currentUser)
        # Hot fix for braket-sw backend retrieval error
        if backendList == []:
            return ResponseModel(
                backendList,
                "Error: Can't fetch backend list from Strangeworks. Please try again later.",
            )
    elif provider == "qfaas":
        backendList = await get_backends_from_db(currentUsername, provider)
        return ResponseModel(
            backendList,
            str(len(backendList))
            + " QFaaS internal backend(s) are fetched successfully.",
        )
    else:
        return ErrorResponseModel(
            "An error occurred.",
            404,
            "Provider ("
            + str(provider)
            + ") doesn't exist or invalid. Please try again.",
        )
    await delete_many_backends(currentUsername, provider)
    backends = await add_many_backends(backendList)
    return ResponseModel(
        backends,
        str(len(backendList))
        + " backends from provider "
        + provider
        + " are fetched successfully.",
    )


@router.get("/{id}", response_description="Backend data retrieved")
async def get_backend_data(id):
    """Get backend information by ID
    Args:
    - **id** (ObjectID): Backend ID (from QFaaS)

    Returns:
        Backend Information
    """
    backend = await retrieve_backend(id)
    if backend:
        return ResponseModel(backend, "Backend data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Backend doesn't exist.")


@router.put("/{id}")
async def update_backend_data(id: str, req: UpdateBackendModel = Body(...)):
    """Update Backend information

    Args:
    - **id** (str): Backend ID
    - **req** (UpdateBackendModel, optional): Backend Information

    """
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_backend = await update_backend(id, req)
    if updated_backend:
        return ResponseModel(
            updated_backend,
            "Backend with ID {} updated successfully".format(id),
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the backend data.",
    )


@router.delete("/{id}", response_description="Backend data deleted from the database")
async def delete_backend_data(id: str):
    """Delete backend by ID

    Args:
    - **id** (str): Backend ID
    """
    deleted_backend = await delete_backend(id)
    if deleted_backend:
        return ResponseModel(
            "Backend with ID: {} removed".format(id), "Backend deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Backend with id {0} doesn't exist".format(id)
    )
