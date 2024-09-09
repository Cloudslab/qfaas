# import strangeworks
# from strangeworks.braket import get_backends, run_circuit, get_circuit_results
from qfaas.database.dbProvider import retrieve_provider
from qfaas.utils.logger import logger
from qfaas.models.backend import BraketSWBackendSchema
from datetime import datetime

braketBackends = [
    {
        "name": "aws.Aspen-11",
        "type": "qpu",
        "vendor": "Rigetti",
        "qubit": 38,
        "supported_gates": ['cz', 'xy', 'ccnot', 'cnot', 'cphaseshift', 'cphaseshift00', 'cphaseshift01', 'cphaseshift10', 'cswap', 'h', 'i', 'iswap', 'phaseshift', 'pswap', 'rx', 'ry', 'rz', 's', 'si', 'swap', 't', 'ti', 'x', 'y', 'z'],
        "region": "us-west-1",
        "status": True,
    },
    {
        "name": "aws.Aspen-M-1",
        "type": "qpu",
        "vendor": "Rigetti",
        "qubit": 80,
        "supported_gates": ['cz', 'xy', 'ccnot', 'cnot', 'cphaseshift', 'cphaseshift00', 'cphaseshift01', 'cphaseshift10', 'cswap', 'h', 'i', 'iswap', 'phaseshift', 'pswap', 'rx', 'ry', 'rz', 's', 'si', 'swap', 't', 'ti', 'x', 'y', 'z'],
        "region": "us-west-1",
        "status": False,
    },
        {
        "name": "aws.Aspen-M-2",
        "type": "qpu",
        "vendor": "Rigetti",
        "qubit": 80,
        "supported_gates": ['cz', 'xy', 'ccnot', 'cnot', 'cphaseshift', 'cphaseshift00', 'cphaseshift01', 'cphaseshift10', 'cswap', 'h', 'i', 'iswap', 'phaseshift', 'pswap', 'rx', 'ry', 'rz', 's', 'si', 'swap', 't', 'ti', 'x', 'y', 'z'],
        "region": "us-west-1",
        "status": False,
    },
    {
        "name": "aws.IonQ Device",
        "type": "qpu",
        "vendor": "IonQ",
        "qubit": 11,
        "supported_gates": ['x', 'y', 'z', 'rx', 'ry', 'rz', 'h', 'cnot', 's', 'si', 't', 'ti', 'v', 'vi', 'xx', 'yy', 'zz', 'swap', 'i'],
        "region": "us-east-1",
        "status": True,
    },
    {
        "name": "aws.Lucy",
        "type": "qpu",
        "vendor": "Oxford Quantum Circuits (OQC)",
        "qubit": 8,
        "supported_gates": ['ccnot', 'cnot', 'cphaseshift', 'cswap', 'cy', 'cz', 'h', 'i', 'phaseshift', 'rx', 'ry', 'rz', 's', 'si', 'swap', 't', 'ti', 'v', 'vi', 'x', 'y', 'z', 'ecr'],
        "region": "eu-west-2",
        "status": True,
    },
    {
        "name": "aws.SV1",
        "type": "simulator",
        "vendor": "Amazon Braket state vector simulator",
        "qubit": 34,
        "supported_gates": [],
        "region": "eu-west-2, us-east-1, us-west-1, us-west-2",
        "status": True,
    },
    {
        "name": "aws.dm1",
        "type": "simulator",
        "vendor": "Amazon Braket density matrix simulator",
        "qubit": 17,
        "supported_gates": [],
        "region": "eu-west-2, us-east-1, us-west-1, us-west-2",
        "status": True,
    }
]

def initialize_SWProvider(swUser, providerToken):
    # try:
    #     logger.info("Authenticate Strangeworks account with username: " + str(swUser))
    #     # strangeworks.authenticate(username=swUser, api_key=providerToken)
    # except Exception as ex:
    #     logger.warning(ex)
    #     return False
    pass

async def get_braketsw_backends(user) -> list:
    # backendList = []
    # username = user['username']
    # providerInfo = await retrieve_provider(username, 'braket-sw')
    # providerToken = providerInfo['providerToken']
    # swUser = providerInfo['additionalInfo']['swUser']
    # initialize_SWProvider(swUser, providerToken)
    # if swUser:
    #     for backend in get_backends():
    #         print(backend)
    #         currentBk = next((item for item in braketBackends if item["name"] == backend), None)
    #         if currentBk:
    #             backendList.append(
    #                 BraketSWBackendSchema(
    #                     name=currentBk.get("name"),
    #                     type=currentBk.get("type"),
    #                     qubit=currentBk.get("qubit"),
    #                     user=user['username'],
    #                     active=currentBk.get("status"),
    #                     sdk="braket",
    #                     backendInfo={
    #                         "swUser": swUser,
    #                         "basis_gates": str(currentBk.get("supported_gates")),
    #                         "vendor": currentBk.get("vendor"),
    #                         "aws_region": currentBk.get("region"),
    #                         "last_updated": str(datetime.now())
    #                     }
    #             )
    #             )
    # return backendList
    pass
    
    