import datetime
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from qfaas.utils.auth import get_user
from qfaas.database.dbUser import retrieve_users
from qfaas.models.auth import TokenData
from qfaas.models.user import UserSchema
from qfaas.core.config import settings

# Customize OpenAPI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    users_db = await retrieve_users()
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserSchema = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user.username


async def get_current_user_token(
    current_user: UserSchema = Depends(get_current_user),
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return {"username": current_user.username, "token": current_user.currentToken}
