from fastapi import APIRouter, Depends

from model.user import User, UserLogin
from config.db import conn
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.user import userEntity, usersEntity
from schemas.auth import authEntity, authenticationEntity
from controller.auth import jwt_handler

userRouter = APIRouter()
db = conn.sight.user
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='tokne')


@userRouter.post("/token")
async def token_generate(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    return {"access_token": form_data.username, "token_type": "bearer"}


@userRouter.get('/auth/authenticate')
async def authenticate(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@userRouter.post('/user/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if checkUser(form_data):
        return {"access_token": jwt_handler.signJWT(form_data.username), "token_type": "bearer"}
    else:
        return {"access_token": None, "token_type": "bearer"}


@userRouter.post('/')
async def create_user(user: User):
    db.insert_one(dict(user))
    return usersEntity(db.find())


def checkUser(data: UserLogin):

    if (userData := db.find_one({"username": data.username, "password": data.password})) is not None:
        return userData
