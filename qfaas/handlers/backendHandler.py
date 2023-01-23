from qfaas.utils.logger import logger
from qfaas.models.backend import BackendRequestSchema, BackendResponseSchema
from qfaas.database.dbBackend import get_backends_from_db
from qfaas.database.dbProvider import retrieve_provider
from qfaas.providers.ibmq import (
    get_least_busy_backend,
    pre_select_ibmq_backend,
    get_ibmq_default_hub,
)
from qfaas.database.dbUser import retrieve_user_token

# Get provider token
async def get_provider_token(user: str, provider: str):
    if provider in ["ibmq", "braket-sw"]:
        provider = await retrieve_provider(user, provider)
        token = provider["providerToken"] if provider["providerToken"] else ""
    elif provider == "qfaas":
        token = await retrieve_user_token(user)
        print(token)
    else:
        token = ""
    return token


async def select_backend(beReq: BackendRequestSchema, currentUser: str):
    beRes = None
    provider = beReq.provider
    if provider == "qfaas":
        beRes = await select_internal_backend(beReq, currentUser)
    elif provider == "ibmq":
        beRes = await select_ibmq_backend(beReq, currentUser)
    elif provider == "braket-sw":
        beRes = await select_braketsw_backend(beReq, currentUser)
    return beRes


async def select_internal_backend(beReq: BackendRequestSchema, currentUser: str):
    beRes = None
    backend = None
    beName = beReq.backendName if beReq.backendName else ""
    backends = await get_backends_from_db(
        user=currentUser, provider=beReq.provider, sdk=beReq.sdk, name=beName
    )
    for be in backends:
        if beReq.type:
            if int(be["qubit"]) >= beReq.rQubit and be["type"] == beReq.type:
                backend = be
                break
        else:
            if int(be["qubit"]) >= beReq.rQubit:
                backend = be
                break
    if backend:
        beRes = BackendResponseSchema(**backend)
        beRes.providerToken = await get_provider_token(currentUser, beReq.provider)
    return beRes


async def select_ibmq_backend(beReq: BackendRequestSchema, currentUser: str):
    beRes = None
    providerToken = await get_provider_token(currentUser, beReq.provider)
    hub = await get_ibmq_default_hub(currentUser)
    # Auto select the backend
    if beReq.autoSelect:
        # Find backend have enough qubit
        preSelectedBackend = await pre_select_ibmq_backend(currentUser, beReq, hub)
        if preSelectedBackend:
            # Get least_busy backend from IBMQ backend
            selectedBackendName = get_least_busy_backend(
                preSelectedBackend, providerToken, hub
            )
            selectedBackend = await get_backends_from_db(
                currentUser, "ibmq", selectedBackendName
            )
            beRes = BackendResponseSchema(**selectedBackend[0])
            beRes.providerToken = providerToken
    else:
        # Check if that backend exists or not
        beRes = await select_internal_backend(beReq, currentUser)
    return beRes


async def select_braketsw_backend(beReq: BackendRequestSchema, currentUser: str):
    # Temp: select the backend from local database
    # TODO: Retrive the job queue from all backends to select least busy backend (when Strangeworks supports)
    if beReq.autoSelect:
        beReq.backendName = ""
    beRes = await select_internal_backend(beReq, currentUser)
    return beRes
