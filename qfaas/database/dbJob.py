from datetime import datetime, time, timedelta
from dateutil import parser
from bson.objectid import ObjectId
from .dbConnect import dbClient
from qfaas.utils.logger import logger


dbJob = dbClient.jobs
job_collection = dbJob.get_collection("jobs_collection")

# Helper format
def job_helper(job) -> dict:
    return {
        "jobId": str(job["_id"]),
        "providerJobId": str(job["providerJobId"]),
        "backend": dict(job["backend"]),
        "status": str(job["status"]),
        "function": str(job["function"]),
        "submitTime": str(job["submitTime"]),  # Parse datetime format
        "lastUpdated": str(job["lastUpdated"]),
        "jobRequest": dict(job["jobRequest"]),
        "owner": str(job["owner"]),
        "result": dict(job["result"]),
        "jobInfo": dict(job["jobInfo"]),
    }


def job_helper_short(job) -> dict:
    return {
        "jobId": str(job["_id"]),
        "providerJobId": str(job["providerJobId"]),
        "backend": dict(job["backend"]),
        "status": str(job["status"]),
        "function": str(job["function"]),
        "submitTime": str(job["submitTime"]),  # Parse datetime format
        "lastUpdated": str(job["lastUpdated"]),
        "owner": str(job["owner"]),
    }


# CRUD operations
# Retrieve all jobs
async def retrieve_jobs():
    jobs = []
    async for job in job_collection.find():
        jobs.append(job_helper_short(job))
    return jobs


# Add a new job into to the database
async def add_job(job_data: dict) -> dict:
    job = await job_collection.insert_one(job_data)
    new_job = await job_collection.find_one({"_id": job.inserted_id})
    return job_helper(new_job)


# Retrieve a job with a matching ID
async def retrieve_job(id: str) -> dict:
    job = await job_collection.find_one({"_id": ObjectId(id)})
    if job:
        return job_helper(job)


# Retrieve a job with a matching username
async def retrieve_jobs_by_username(username: str) -> dict:
    jobs = []
    async for job in job_collection.find({"owner": str(username)}):
        jobs.append(job_helper_short(job))
    return jobs


# Retrieve a job with a multiple criteria
async def retrieve_jobs_by_multiple_criteria(filter: dict) -> dict:
    jobs = []
    # Get rid of the None value
    filter = {k: v for k, v in filter.items() if v is not None}
    # logger.info(filter)
    async for job in job_collection.find({"$and": [filter]}):
        jobs.append(job_helper_short(job))
    return jobs


# Update a job with a matching ID
async def update_job(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    job = await job_collection.find_one({"_id": ObjectId(id)})
    if job:
        updated_job = await job_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_job:
            return await retrieve_job(id)
        return False


# Delete a job from the database by Id
async def delete_job(id: str):
    job = await job_collection.find_one({"_id": ObjectId(id)})
    if job:
        await job_collection.delete_one({"_id": ObjectId(id)})
        return True


# Delete all job from the database by owner
async def delete_job_by_owner(username: str):
    filter = {"owner": str(username)}
    job = await job_collection.find_one(filter)
    if job:
        count = await job_collection.delete_many(filter)
        return count.deleted_count
    return 0
