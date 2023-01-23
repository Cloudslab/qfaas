from cgitb import handler
import os
import json
import subprocess
import base64
import requests
from fastapi import Depends
from requests.auth import HTTPBasicAuth
from qfaas.core.config import settings
from qfaas.handlers.userHandler import get_role
from qfaas.dependency.auth import get_current_active_user, get_current_user_token
from qfaas.utils.logger import logger
from datetime import datetime
from qfaas.models.function import (
    FunctionSchema,
    FunctionInvocationSchema,
    ScaleFunctionModel,
)
from fastapi.encoders import jsonable_encoder

from qfaas.models.job import JobSchema
from qfaas.database.dbFunction import (
    add_function,
    update_function_db,
    delete_function_db,
    retrieve_function,
    retrieve_functions,
)

from qfaas.database.dbJob import update_job, add_job

from qfaas.handlers.jobHandler import (
    create_job,
)


def function_helper(function) -> dict:
    return {
        "name": str(function["name"]),
        "template": str(function["template"]),
        "requirements": str(function["requirements"]),
        "handlerPy": dict(function["handlerPy"]),
        "handlerQs": str(function["handlerQs"]),
    }


def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True, text=True)
    exit_code = p.wait()
    return (p.stdout.read(), exit_code)


def is_json(myjson):
    try:
        json.loads(myjson)
    except:
        return False
    return True


def encode_base64(text):
    message_bytes = text.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode("ascii")


def pull_function():
    cmd = "git pull"
    detail, err = system_call(cmd)
    if err != 0:
        return detail, err
    return "Create success!", 0


def up_function(name):
    cmd = 'echo "' + name + '" > build.txt'
    detail, err = system_call(cmd)
    if err != 0:
        return detail, err

    cmd = "git checkout " + settings.GIT_BRANCH
    detail, err = system_call(cmd)
    if err != 0:
        return detail, err

    cmd = "git add ."
    detail, err = system_call(cmd)
    if err != 0:
        return detail, err

    cmd = 'git commit -m "Push function ' + name + '"'
    detail, err = system_call(cmd)
    if err != 0:
        return detail, err

    cmd = "git push origin " + settings.GIT_BRANCH
    detail, err = system_call(cmd)
    if err != 0:
        return detail, err
    return "Up success!", 0


def create_function(function_data: FunctionSchema):

    name = function_data.name
    template = function_data.template
    name = template + "-" + name

    PATH_FUNCTION = settings.ROOT_PATH + "qfaas-fn/functions"
    os.chdir(PATH_FUNCTION)
    detail, err = pull_function()
    if err != 0:
        return detail, err

    cmd = (
        "faas-cli "
        + "new "
        + "--lang "
        + template
        + " "
        + name
        + " --append=./functions.yml "
        + "--prefix="
        + settings.DOCKER_REPOSITORY
    )
    detail, err = system_call(cmd)
    if err != 0:
        return detail, err

    if function_data.fnCode.requirements is not None:
        path = settings.ROOT_PATH + "qfaas-fn/functions/" + name + "/requirements.txt"
        f = open(path, "w")
        f.write(base64.b64decode(function_data.fnCode.requirements).decode("utf-8"))
        f.close()

    if function_data.fnCode.handlerPy is not None:
        path = settings.ROOT_PATH + "qfaas-fn/functions/" + name + "/handler.py"
        f = open(path, "w")
        f.write(base64.b64decode(function_data.fnCode.handlerPy).decode("utf-8"))
        f.close()

    if function_data.fnCode.handlerQs is not None:
        path = settings.ROOT_PATH + "qfaas-fn/functions/" + name + "/handler.qs"
        f = open(path, "w")
        f.write(base64.b64decode(function_data.fnCode.handlerQs).decode("utf-8"))
        f.close()

    detail, err = up_function(name)
    if err != 0:
        return detail, err
    return "Create success!", 0


def get_functions():
    url = settings.QFAAS_URL + "/system/functions"
    response = requests.request(
        "GET", url, auth=HTTPBasicAuth(settings.QFAAS_USER, settings.QFAAS_PASSWORD)
    )
    return json.loads(response.text)


def get_function(name) -> dict:
    PATH_FUNCTION = settings.ROOT_PATH + "qfaas-fn/functions"
    os.chdir(PATH_FUNCTION)
    detail, err = pull_function()
    if err != 0:
        return detail, err

    err = os.path.isdir(PATH_FUNCTION + "/" + name)
    if err != True:
        return None

    template = name.split("-")[0]
    try:
        path = settings.ROOT_PATH + "qfaas-fn/functions/" + name + "/handler.py"
        f = open(path, "r")
        handlerPy = encode_base64(f.read())
        f.close()
    except:
        handlerPy = ""

    try:
        path = settings.ROOT_PATH + "qfaas-fn/functions/" + name + "/handler.qs"
        f = open(path, "r")
        handlerQs = encode_base64(f.read())
        f.close()
    except:
        handlerQs = ""

    try:
        path = settings.ROOT_PATH + "qfaas-fn/functions/" + name + "/requirements.txt"
        f = open(path, "r")
        requirements = encode_base64(f.read())
        f.close()
    except:
        requirements = ""
    result = {
        "fnTemplate": str(template),
        "fnCode": {
            "requirements": str(requirements),
            "handlerPy": str(handlerPy),
            "handlerQs": str(handlerQs),
        },
    }
    url = settings.QFAAS_URL + "/system/function/" + name

    response = requests.request(
        "GET", url, auth=HTTPBasicAuth(settings.QFAAS_USER, settings.QFAAS_PASSWORD)
    )
    data = json.loads(response.text)
    data.update(result)
    return data


def update_function(function_data: FunctionSchema):
    name = function_data.name

    PATH_FUNCTION = settings.ROOT_PATH + "qfaas-fn/functions"
    os.chdir(PATH_FUNCTION)
    detail, err = pull_function()
    if err != 0:
        return detail, err

    if function_data.fnCode.requirements is not None:
        path = settings.ROOT_PATH + "qfaas-fn/functions/" + name + "/requirements.txt"
        f = open(path, "w")
        f.write(base64.b64decode(function_data.fnCode.requirements).decode("utf-8"))
        f.close()

    if function_data.fnCode.handlerPy is not None:
        path = settings.ROOT_PATH + "qfaas-fn/functions/" + name + "/handler.py"
        f = open(path, "w")
        f.write(base64.b64decode(function_data.fnCode.handlerPy).decode("utf-8"))
        f.close()

    if function_data.fnCode.handlerQs is not None:
        path = settings.ROOT_PATH + "qfaas-fn/functions/" + name + "/handler.qs"
        f = open(path, "w")
        f.write(base64.b64decode(function_data.fnCode.handlerQs).decode("utf-8"))
        f.close()

    detail, err = up_function(name)
    if err != 0:
        return detail, err
    return "Update success!", 0


def delete_function(name):
    PATH_FUNCTION = settings.ROOT_PATH + "qfaas-fn/functions"
    os.chdir(PATH_FUNCTION)
    detail, err = pull_function()
    if err != 0:
        return detail, err

    err = os.path.isdir(PATH_FUNCTION + "/" + name)
    if err != True:
        return None

    cmd = (
        "awk -i inplace -v n=1 -v tag='"
        + name
        + ":' '/^  [^ ]/{n=1} /^  [^ ]/ && $1==tag {n=0} n' functions.yml"
    )
    system_call(cmd)

    cmd = "sed '/^" + name + "$/d' build.txt"
    system_call(cmd)

    cmd = "rm -rf " + name
    system_call(cmd)

    url = settings.QFAAS_URL + "/system/functions"
    payload = '{\r\n  "functionName": "' + name + '"\r\n}'
    headers = {"Content-Type": "text/plain"}
    response = requests.request(
        "DELETE",
        url,
        headers=headers,
        data=payload,
        auth=HTTPBasicAuth(settings.QFAAS_USER, settings.QFAAS_PASSWORD),
    )

    detail, err = up_function(name)
    return True


# Invoke function handler
async def invoke_function(
    name: str, req: FunctionInvocationSchema, currentUserUsername: str, token: str
) -> dict:
    # TEMP - Get service API URL
    if req.local:
        # For local development - temporarily
        url = settings.QFAAS_URL + "/function/" + name # https://qfaas.cloud/function/FNNAME
    else:
        # For production
        url = "http://" + name + settings.QFAAS_FUNCTION_URL + "/" #FNNAME.openfaas-fn.svc.cluster.local:8080

    # 1. Prepare the request data
    request = {k: v for k, v in req.dict().items() if v is not None}
    payload = json.dumps(request)
    headers = {"Content-Type": "application/json", "Authorization": token}

    # 2. Forward request to the service
    submitTime = str(datetime.now())
    response = requests.request("POST", url, headers=headers, data=payload)
    result = response.json()  # dict
    jobResult = result.get("jobResult")
    if jobResult is None:
        jobResult = {}
    if type(jobResult) is not dict:
        jobResult = {"data": jobResult}

    # If postProcessOnly is True => get Result and update to existing job, don't create new job
    if req.postProcessOnly:
        if jobResult:
            status = "DONE"
        else:
            status = "ERROR"
        updatedJob = {
            "lastUpdated": str(datetime.now()),
            "status": status,
            "result": jobResult,
        }
        jobData = await update_job(req.jobId, updatedJob)
    else:
        # 3. Create job data
        job = JobSchema(
            providerJobId=result.get("providerJobId"),
            provider=req.provider,
            backend=result.get("backend"),
            owner=currentUserUsername,
            function=name,
            jobRequest=request,
            result=jobResult,
            submitTime=submitTime,
            lastUpdated=str(datetime.now()),
            status=result.get("jobStatus")["status"],
        )
        job = jsonable_encoder(job)
        jobData = await add_job(job)
    return jobData


async def check_function_permission(nameFunction, currentUserUsername) -> bool:
    infoFunction = await retrieve_function(nameFunction)
    roleCurrentUser = await get_role(currentUserUsername)
    if roleCurrentUser == "admin":
        return True
    elif roleCurrentUser == "dev" and infoFunction["author"] == currentUserUsername:
        return True
    else:
        return False


async def check_function_permission_invoke(nameFunction, currentUserUsername) -> bool:
    infoFunction = await retrieve_function(nameFunction)
    roleCurrentUser = await get_role(currentUserUsername)
    if roleCurrentUser == "admin":
        return True
    elif (
        infoFunction["author"] == currentUserUsername or infoFunction["public"] == True
    ):
        return True
    else:
        return False


def function_helper(function) -> dict:

    try:
        invocationCount = int(function["invocationCount"])
    except:
        invocationCount = 0

    try:
        secrets = list(function["secrets"])
    except:
        secrets = []

    return {
        "name": str(function["name"]),
        "image": str(function["image"]),
        "invocationCount": invocationCount,
        "status": int(function["status"]),
        "author": str(function["author"]),
        "public": bool(function["public"]),
        "fnTemplate": str(function["name"]).split("-")[0],
        "replicas": int(function["replicas"]),
        "fnConfig": {"secrets": secrets},
    }


def function_helper_get(function) -> dict:

    try:
        invocationCount = int(function["invocationCount"])
    except:
        invocationCount = 0

    try:
        handlerPy = str(function["fnCode"]["handlerPy"])
    except:
        handlerPy = ""

    try:
        handlerQs = str(function["fnCode"]["handlerQs"])
    except:
        handlerQs = ""

    try:
        requirements = str(function["fnCode"]["requirements"])
    except:
        requirements = ""

    try:
        secrets = list(function["secrets"])
    except:
        secrets = []

    return {
        "name": str(function["name"]),
        "image": str(function["image"]),
        "invocationCount": invocationCount,
        "status": int(function["status"]),
        "fnCode": {
            "handlerPy": handlerPy,
            "handlerQs": handlerQs,
            "requirements": requirements,
        },
        "author": str(function["author"]),
        "public": bool(function["public"]),
        "fnTemplate": str(function["author"]),
        "replicas": int(function["replicas"]),
        "fnConfig": {"secrets": secrets},
    }


def scale_function(name: str, req: ScaleFunctionModel):
    url = settings.QFAAS_URL + "/system/scale-function/" + name
    req = {k: v for k, v in req.dict().items() if v is not None}
    payload = json.dumps(req)
    headers = {"Content-Type": "application/json"}
    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=payload,
        auth=HTTPBasicAuth(settings.QFAAS_USER, settings.QFAAS_PASSWORD),
    )
    return response.status_code


def get_status_function(name: str) -> dict:
    cmd = "kubectl get deployment " + name + " -n openfaas-fn -o json"
    detail, err = system_call(cmd)
    if err != 0:
        return {"status": 0}
    try:
        resutl = json.loads(detail)
        return {"status": resutl["status"]["availableReplicas"]}
    except:
        return {"status": 0}
