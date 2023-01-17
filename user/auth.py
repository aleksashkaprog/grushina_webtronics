import sqlite3

from jose import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from .services import (
    ALGORITHM,
    JWT_SECRET_KEY
)

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reusable_oauth2)):
    payload = jwt.decode(
            token, JWT_SECRET_KEY, ALGORITHM
        )
    with sqlite3.connect('sqlite.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users "
            "WHERE username=?",
            (payload['sub'],)
        )
        user = cursor.fetchone()

    return user
