from pydantic import BaseModel
from datetime import datetime
from src.schemas.user import User


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    dev: bool


class UserLogin(BaseModel):
    username: str
    password: str


class UserInDB(BaseModel):
    username: str
    email: str
    hashed_password: str


class SignInResponse(BaseModel):
    access_token: str
    expiration: datetime
    user_info: User
