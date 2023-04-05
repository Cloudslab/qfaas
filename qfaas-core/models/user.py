from typing import Optional

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    username: str = Field(...)
    hashedPassword: str = Field(...)
    role: Optional[str] = None
    currentToken: Optional[str] = None
    disabled: Optional[bool] = None
    displayName: Optional[str] = "QFaaS New User"

    class Config:
        schema_extra = {"example": {"username": "qfaas", "password": "password_here"}}


class UserSignUpModel(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    displayName: Optional[str] = "QFaaS New User"

    class Config:
        schema_extra = {
            "example": {
                "username": "qfaas",
                "password": "password_here",
                "displayName": "New Member",
            }
        }


class UpdateUserModel(BaseModel):
    disabled: Optional[bool] = None
    displayName: Optional[str] = None
    newPassword: Optional[str] = None
    newPasswordConfirm: Optional[str] = None
    currentPassword: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "displayName": "QFaaS New name",
                "currentPassword": "",
                "newPassword": "",
                "newPasswordConfirm":"",
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
