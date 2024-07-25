# From Python 3.9, don't need import Dict from typing
from typing import Optional

from pydantic import BaseModel, Field


class BackendSchema(BaseModel):
    # Field(...) means this is required
    name: str = Field(..., title="Name of the backend")
    provider: str = Field(...)
    type: str | None
    qubit: int | None = 0
    user: str = Field(...)
    active: bool | None
    sdk: str = Field(...)  # Type of supported SDK
    backendInfo: dict | None = None

    class Config:
        schema_extra = {
            "example": {
                "name": "qiskit_simulator",
                "provider": "qfaas",
                "type": "simulator",
                "qubit": 30,
                "user": "hoant",
                "active": True,
                "sdk": "qiskit",
                "backendInfo": {"hub": "ibm-q"},
            }
        }


class UpdateBackendModel(BaseModel):
    # For Python 3.10+ only
    # Optional[str] in Python 3.6+ = str | None in Python 3.10+
    name: str | None
    provider: str | None
    type: str | None
    qubit: int | None
    user: str | None
    active: bool | None
    sdk: str | None
    backendInfo: dict | None

    class Config:
        schema_extra = {
            "example": {
                "name": "qiskit_simulator",
                "provider": "qfaas",
                "type": "simulator",
                "qubit": 30,
                "user": "hoant",
                "active": True,
                "sdk": "qiskit",
                "backendInfo": {"hub": "ibm-q"},
            }
        }


class IBMQBackendSchema(BackendSchema):
    provider: str = "ibmq"


class BraketSWBackendSchema(BackendSchema):
    provider: str = "braket-sw"


class BackendResponseSchema(BackendSchema):
    providerToken: str = ""


class BackendRequestSchema(BaseModel):
    sdk: str = Field(...)
    provider: str = Field(...)
    rQubit: Optional[int] = 1
    type: Optional[str]
    autoSelect: Optional[bool] = False
    backendName: Optional[str]
    # extraInfo: Optional[dict]

    class Config:
        schema_extra = {
            "example": {
                "sdk": "qiskit",
                "provider": "ibmq",
                "rQubit": 5,
                "type": "qpu",
                "autoSelect": 1,
                "backendName": ""
                # "extraInfo": {},
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
