from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class JobSchema(BaseModel):
    providerJobId: Optional[str]
    provider: str = Field(...)
    backend: dict = Field(...)
    status: str = Field(...)
    owner: str = Field(...)
    function: str = Field(...)
    submitTime: datetime = Field(...)  # HH:MM[:SS[.ffffff]][Z or [±]HH[:]MM]]]
    lastUpdated: datetime = Field(...)
    jobRequest: dict = Field(...)
    result: Optional[dict] = {}
    jobInfo: Optional[dict] = {}

    class Config:
        schema_extra = {
            "example": {
                "providerJobId": "abc12345",
                "provider": "ibmq",
                "backend": "ibmq_qasm_simulator",
                "status": "CREATED",
                "owner": "qfaas",
                "function": "qiskit-qrng",
                "submitTime": "2022-04-23T10:20:30.400+02:30",
                "lastUpdated": "2022-04-23T10:20:40.400+02:30",
                "jobRequest": {"input": "12", "additional": "Sample info"},
                "result": {
                    "result": "1234",
                    "raw_result": "100010",
                    "additional": "Sample info",
                },
                "jobInfo": {"info1": "Sample info 1", "info2": "Sample info 2"},
            }
        }


class UpdateJobModel(BaseModel):
    providerJobId: Optional[str]
    provider: Optional[str]
    backend: Optional[str]
    status: Optional[str]
    owner: Optional[str]
    function: Optional[str]
    submitTime: Optional[datetime]  # HH:MM[:SS[.ffffff]][Z or [±]HH[:]MM]]]
    lastUpdated: Optional[datetime]
    jobRequest: Optional[dict]
    result: Optional[dict]
    jobInfo: Optional[dict]

    class Config:
        schema_extra = {
            "example": {
                "providerJobId": "abc12345",
                "provider": "ibmq",
                "backend": "ibmq_qasm_simulator",
                "status": "CREATED",
                "owner": "qfaas",
                "function": "qiskit-qrng",
                "submitTime": "2022-04-23T10:20:30.400+02:30",
                "lastUpdated": "2022-04-23T10:20:40.400+02:30",
                "jobRequest": {"input": "12", "additional": "Sample info"},
                "result": {
                    "result": "1234",
                    "raw_result": "100010",
                    "additional": "Sample info",
                },
                "jobInfo": {"info1": "Sample info 1", "info2": "Sample info 2"},
            }
        }


class FilterJobModel(BaseModel):
    jobId: Optional[str]
    providerJobId: Optional[str]
    provider: Optional[str]
    backend: Optional[str]
    status: Optional[str]
    function: Optional[str]
    submitTime: Optional[datetime]  # HH:MM[:SS[.ffffff]][Z or [±]HH[:]MM]]]
    lastUpdated: Optional[datetime]
    owner: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "jobId": "62709b67c81dd215de1324fb",
                "providerJobId": "abc12345",
                "provider": "ibmq",
                "backend": "external",
                "status": "completed",
                "function": "qiskit-qrng",
                "submitTime": "2022-04-23T10:20:30.400+02:30",
                "lastUpdated": "2022-04-23T10:20:40.400+02:30",
                "owner": "qfaas-admin",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
