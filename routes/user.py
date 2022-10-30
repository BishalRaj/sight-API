from fastapi import APIRouter

from model.user import User
from config.db import conn
from schemas.user import usersEntity

user = APIRouter()


@user.get('/')
async def login():
    return usersEntity(conn.local.user.find())
