from qiskit import IBMQ
from qiskit.providers.ibmq.managed import IBMQJobManager
from qiskit.providers.ibmq import least_busy
from qfaas.utils.logger import logger
from qfaas.models.backend import IBMQBackendSchema
from qfaas.database.dbProvider import retrieve_provider
from datetime import datetime
from qfaas.models.job import JobSchema
from qfaas.models.backend import BackendRequestSchema
from qfaas.database.dbBackend import get_backends_from_db
import time


def initialize_IBMQProvider(ibmqToken: str, hub: str = "ibm-q"):
    """Initialize IBMQ Provider

    Args:
        ibmqToken (str): IBMQ API token
        hub (str, optional): hub name. Defaults to "ibm-q".

    Returns:
        IBMQ AccountProvider
    """
    try:
        # Check current session
        if IBMQ.active_account():
            if IBMQ.active_account()["token"] == ibmqToken:
                IBMQProvider = IBMQ.get_provider(hub=hub)
                logger.info("Used current IBMQ Provider, hub " + hub)
            else:
                IBMQ.disable_account()
                IBMQProvider = IBMQ.enable_account(ibmqToken, hub=hub)
                logger.info("Changed current session to new IBMQ Provider, hub " + hub)
        else:
            IBMQProvider = IBMQ.enable_account(ibmqToken, hub=hub)
            logger.info("Enabled new IBMQ Provider, hub " + hub)
    except Exception as ex:
        logger.warning(ex)
        return None
    return IBMQProvider


def get_IBMQ_hubs(ibmqToken: str):
    """Verify IBMQ account and return list of available hubs

    Args:
        ibmqToken (str): IBMQ Token

    Returns:
        List of available hubs or [] if IBMQ Account is not correct
    """
    ibmq = initialize_IBMQProvider(ibmqToken)
    hubs = []
    if ibmq:
        # Get all available hubs and store them in the database
        providers = IBMQ.providers()
        for pv in providers:
            if pv.backends()[0]:
                hubs.append(pv.backends()[0].hub)
        return hubs
    return hubs


# Get default hub
async def get_ibmq_default_hub(user: str):
    provider = await retrieve_provider(user, "ibmq")
    hub = (
        provider["additionalInfo"]["defaultHub"]
        if provider["additionalInfo"]["defaultHub"]
        else "ibm-q"
    )
    return hub


# Pre-filter the approriate IBMQ Backend from the database
async def pre_select_ibmq_backend(
    currentUser: str, beReq: BackendRequestSchema, hub: str
):
    # Check if that backend exists or not
    backends = await get_backends_from_db(user=currentUser, provider="ibmq")
    backend = []
    for bk in backends:
        if beReq.type:
            if (
                int(bk["qubit"]) >= beReq.rQubit
                and bk["type"] == beReq.type
                and bk["backendInfo"]["hub"] == hub
            ):
                backend.append(bk["name"])
        else:
            if int(bk["qubit"]) >= beReq.rQubit and bk["backendInfo"]["hub"] == hub:
                backend.append(bk["name"])
    return backend


async def get_ibmq_backends(user, hub: str) -> list:
    backendList = []
    username = user["username"]
    providerInfo = await retrieve_provider(username, "ibmq")
    providerToken = providerInfo["providerToken"]
    provider = initialize_IBMQProvider(ibmqToken=providerToken, hub=hub)
    for backend in provider.backends():
        try:
            backendList.append(
                IBMQBackendSchema(
                    name=backend.name(),
                    type="simulator"
                    if backend.configuration().simulator is True
                    else "qpu",
                    qubit=backend.configuration().n_qubits,
                    user=username,
                    active=backend.status().operational,
                    sdk="qiskit",
                    backendInfo={
                        "hub": backend.hub,
                        "group": backend.group,
                        "project": backend.project,
                        "basis_gates": str(backend.configuration().basis_gates),
                        "last_updated": str(datetime.now()),
                    },
                )
            )
        except Exception as ex:
            logger.warning(ex)
            continue
    return backendList


async def check_job_result(user, backend, hub, jobId):
    username = user["username"]
    providerInfo = await retrieve_provider(username, "ibmq")
    providerToken = providerInfo["providerToken"]
    provider = initialize_IBMQProvider(ibmqToken=providerToken, hub=hub)
    backend = provider.get_backend(backend)
    job = backend.retrieve_job(jobId)
    jobStatus = ibmq_job_monitor(job, 2, 5)
    jobResult = None
    if jobStatus.get("status") == "DONE":
        counts = job.result()
        jobResult = dict(counts.get_counts())
    return {
        "providerJobId": job.job_id(),
        "jobStatus": jobStatus,
        "backend": {"name": job.backend().name(), "hub": job.backend().hub},
        "jobResult": jobResult,
    }


def ibmq_job_monitor(job, interval: int, max_iterations: int):
    """Monitor job status at IBM Quantum

    Args:
    - job (IBMQJob): Job instance
    - interval (int): Interval time to check job status (in seconds)

    Returns:
    - Job status
    """
    status = job.status()
    iteration = 0
    # max_iterations = 10 # Maximum number of iterations to check

    while status.name not in ["DONE", "CANCELLED", "ERROR"]:
        time.sleep(interval)
        status = job.status()
        msg = status.value
        if status.name == "QUEUED":
            details = msg + " (%s)" % job.queue_position()
        iteration += 1
        if iteration >= max_iterations:
            break
    msg = status.value
    details = msg
    jobStatus = {"status": status.name, "details": details}
    return jobStatus


def get_least_busy_backend(preSelectedBackend: list, providerToken: str, hub: str):
    provider = initialize_IBMQProvider(ibmqToken=providerToken, hub=hub)
    backends = []
    logger.info(
        "Select least busy backend in the following candidates: "
        + str(preSelectedBackend)
    )
    for bk in preSelectedBackend:
        backends.append(provider.get_backend(bk))
    try:
        selectedBackend = least_busy(backends).name()
    except Exception as e:
        logger.error(e)
    return selectedBackend
