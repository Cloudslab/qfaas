from fastapi import APIRouter, Body, Depends, Request
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from qfaas.database.dbJob import (
    add_job,
    update_job,
    delete_job,
    delete_job_by_owner,
    retrieve_job,
    retrieve_jobs,
    retrieve_jobs_by_username,
    retrieve_jobs_by_multiple_criteria,
)
from qfaas.models.job import (
    ErrorResponseModel,
    ResponseModel,
    JobSchema,
    UpdateJobModel,
    FilterJobModel,
)

from qfaas.handlers.functionHandler import invoke_function
from qfaas.providers.ibmq import check_job_result
from qfaas.dependency.auth import get_current_active_user

from qfaas.models.user import UserSchema
from qfaas.models.function import FunctionInvocationSchema
from qfaas.database.dbUser import retrieve_user

router = APIRouter()


@router.post("/", response_description="Job data added into the database")
async def add_job_data(job: JobSchema = Body(...)):
    job = jsonable_encoder(job)
    new_job = await add_job(job)
    return ResponseModel(new_job, "Job added successfully.")


@router.get("/", response_description="Jobs retrieved")
async def get_jobs():
    jobs = await retrieve_jobs()
    if jobs:
        return ResponseModel(jobs, "{} jobs retrieved successfully".format(len(jobs)))
    return ResponseModel(jobs, "Empty list returned")


# Get job by Job ID
@router.get("/{id}", response_description="Job data retrieved")
async def get_job_data(
    id, request: Request, current_user: UserSchema = Depends(get_current_active_user)
):
    job = await retrieve_job(id)
    if job:
        # If job status is queued, check job result => then update submit jobrawresult to function for post processing
        if job.get("status") not in ["DONE", "CANCELLED", "ERROR"]:
            currentUser = await retrieve_user(current_user)
            backend = job.get("backend")
            jobResult = await check_job_result(
                currentUser, backend["name"], backend["hub"], job.get("providerJobId")
            )
            # If status = DONE, submit request to post processing
            if jobResult.get("jobStatus")["status"] == "DONE":
                jobRequest = job.get("jobRequest")
                jobRequest["postProcessOnly"] = True
                jobRequest["jobRawResult"] = jobResult.get("jobResult")
                jobRequest["jobId"] = job.get("jobId")
                jobRequest["backendName"] = backend["name"]
                # Send this request to function
                token = request.headers["Authorization"]
                ##### FOR LOCAL TEST ONLY, remove this except for the production
                try:
                    invocationRequest = FunctionInvocationSchema(**jobRequest)
                    await invoke_function(
                        job.get("function"), invocationRequest, job.get("owner"), token
                    )
                except:
                    jobRequest["local"] = True
                    invocationRequest = FunctionInvocationSchema(**jobRequest)
                    await invoke_function(
                        job.get("function"), invocationRequest, job.get("owner"), token
                    )

                job = await retrieve_job(id)
            else:
                updatedInfo = {
                    "status": jobResult.get("jobStatus")["status"],
                    "lastUpdated": str(datetime.now()),
                }
                job = await update_job(id, updatedInfo)
        return ResponseModel(job, "Job data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Job doesn't exist.")


# Get jobs list by username (owner)
@router.get("/owner/{username}", response_description="Job data retrieved")
async def get_jobs_by_owner(
    username, current_user: UserSchema = Depends(get_current_active_user)
):
    currentUser = await retrieve_user(current_user)
    if currentUser.get("role") == "admin":
        job = await retrieve_jobs_by_username(username)
        if job:
            return ResponseModel(job, "{} jobs retrieved successfully".format(len(job)))
        return ErrorResponseModel("An error occurred.", 404, "No jobs found.")
    return ErrorResponseModel(
        "An error occurred",
        404,
        "No permission to retrieve all jobs from other users".format(username),
    )


# Get and filter jobs by multiple criteria
@router.post("/filter", response_description="Jobs data retrieved")
async def filter_jobs_by_multiple_criteria(filter: FilterJobModel = Body(...)):
    filter = jsonable_encoder(filter)
    job = await retrieve_jobs_by_multiple_criteria(filter)
    if job:
        return ResponseModel(job, "{} jobs retrieved successfully".format(len(job)))
    return ErrorResponseModel("An error occurred.", 404, "No jobs found")


@router.put("/{id}")
async def update_job_data(id: str, req: UpdateJobModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_job = await update_job(id, req)
    if updated_job:
        return ResponseModel(
            "Job with ID: {} name update is successful".format(id),
            "Job updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the job data.",
    )


@router.delete("/{id}", response_description="Job data deleted from the database")
async def delete_job_data(id: str):
    deleted_job = await delete_job(id)
    if deleted_job:
        return ResponseModel(
            "Job with ID: {} removed".format(id), "Job deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Job with id {0} doesn't exist".format(id)
    )


@router.delete(
    "/owner/{username}", response_description="Job data deleted from the database"
)
async def delete_job_data_by_owner(
    username: str, current_user: UserSchema = Depends(get_current_active_user)
):
    """Delete multiple jobs by the given username (for Administrator only)

    Args:
    - username (str): job owner

    Returns: Number of deleted jobs
    """
    currentUser = await retrieve_user(current_user)
    if currentUser.get("role") == "admin":
        deletedJobCount = await delete_job_by_owner(username)
        if deletedJobCount:
            return ResponseModel(
                str(deletedJobCount)
                + " job from user {} succesfully deleted".format(username),
                "Job deleted successfully",
            )
        else:
            return ErrorResponseModel(
                "An error occurred",
                404,
                "No job with user {} found. Do nothing".format(username),
            )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "No permission to delete all jobs from other users".format(username),
    )
