from fastapi import APIRouter, Depends

from model.user import User
from config.db import conn
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.user import userEntity, usersEntity

userRouter = APIRouter()
db = conn.sight.user
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='tokne')


@userRouter.post('/auth/login')
# async def login(user: User):
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # return usersEntity(db.find())

    print(form_data)
    return {'access_token': form_data.email+'token'}


@userRouter.post('/')
async def create_user(user: User):
    db.insert_one(dict(user))
    return usersEntity(db.find())
