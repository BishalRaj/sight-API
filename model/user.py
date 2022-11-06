from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    name: str = Field(default=None)
    username: EmailStr = Field(default=None)
    password: str = Field(default=None)


class UserLogin(BaseModel):
    username: EmailStr = Field(default=None)
    password: str = Field(default=None)
