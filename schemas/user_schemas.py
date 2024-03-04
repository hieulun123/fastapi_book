from pydantic import BaseModel


class User(BaseModel):
    email: str


class UserCreate(User):
    password: str


class UserAuth(UserCreate):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
