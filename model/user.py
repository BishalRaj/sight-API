from lib2to3.pytree import Base
from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str
