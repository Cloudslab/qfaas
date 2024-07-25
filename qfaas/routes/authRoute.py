from curses.ascii import isalnum
from datetime import datetime, timedelta
from turtle import update
from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from qfaas.utils.auth import authenticate_user, create_access_token, check_existed_user
from qfaas.models.auth import Token, SignUpResponseModel, ErrorSignUpResponseModel
from qfaas.core.config import settings
from qfaas.models.user import UserSignUpModel
from qfaas.database.dbUser import add_user, retrieve_users, update_user, retrieve_user, update_user_token
from fastapi.encoders import jsonable_encoder
import html

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Input sanitization (check to make sure username does not have any invalid characters)
    sUsername = html.escape(form_data.username)
    if not sUsername.isalnum():
        raise HTTPException(
            status_code=400,
            detail="Invalid username (only alphanumeric characters is allowed). Please check again",
            headers={"WWW-Authenticate": "Bearer"},
        )
    userDb = await retrieve_user(sUsername)
    if userDb:
        user = authenticate_user(userDb, form_data.password)
        if user:
            access_token_expires = timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
            access_token = create_access_token(
                data={"sub": user.get("username")}, expires_delta=access_token_expires
            )
            insertedToken = {"currentToken": access_token}
            await update_user_token(user.get("username"), insertedToken)
            return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


# @router.post("/logout", response_model=Token)
# async def logout():
#     return "Coming soon..."


# @router.post("/resetToken", response_model=Token)
# async def reset_token():
#     return "Coming soon..."


@router.post("/signup")
async def sign_up(user: UserSignUpModel = Body(...)):
    user = jsonable_encoder(user)
    users_db = await retrieve_users()
    if check_existed_user(users_db, user["username"]):
        return ErrorSignUpResponseModel(
            "An error occurred", 400, "Username was existed"
        )
    new_user = await add_user(user)
    return SignUpResponseModel(new_user, "Sign up successfully!")
