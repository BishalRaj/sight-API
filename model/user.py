from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str = None
    email: EmailStr
    password: str
