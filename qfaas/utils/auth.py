from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import jwt
from qfaas.models.user import UserSchema
from qfaas.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(userDb, password: str):
    if not verify_password(password, userDb.get("hashedPassword")):
        return False
    return userDb


def verify_password(plain_password, hashedPassword):
    return pwd_context.verify(plain_password, hashedPassword)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(users_db, username: str):
    for user in users_db:
        if user["username"] == username:
            user_dict = user
            return UserSchema(**user_dict)


def check_existed_user(users_db, username: str):
    for user in users_db:
        if user["username"] == username:
            return True
    return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def detroy_access_token(token: str):
    return token
