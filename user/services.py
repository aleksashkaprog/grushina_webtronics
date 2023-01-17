import sqlite3
from typing import Union, Any

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

from .models import User
from .schemas import UserCreate

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = 'gudrfgrwie473294thbgoe9238t2go3t2g9ybg2o92438g'
JWT_REFRESH_SECRET_KEY = '579637hg9qh9lwg3rvqo3w4h5ho3593e03450g3gp32gq'
access_token_jwt_subject = "access"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


async def save_user(
        username: str,
        password: str
):
    info = UserCreate(username=username, password=password)
    return await User.objects.create(**info.dict())


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def get_user_login(
        username: str,
        password: str,
):
    with sqlite3.connect('sqlite.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users "
            "WHERE username=? AND password=?;",
            (username, password)
        )
        user = cursor.fetchone()

    return user
