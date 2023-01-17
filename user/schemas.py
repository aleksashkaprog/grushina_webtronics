from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class UserAuth(BaseModel):
    username: str = Field(..., description="username")
    password: str = Field(..., min_length=5, max_length=24, description="user password")


class UserOut(BaseModel):
    id: str
    username: str


class UserCreate(BaseModel):
    username: str
    password: str


class SystemUser(UserOut):
    password: str
