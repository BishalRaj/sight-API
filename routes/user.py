from http.client import HTTPException
from fastapi import APIRouter, Depends
from model.user import User, UserLogin
from config.db import conn
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.user import userEntity, usersEntity
from schemas.auth import authEntity, authenticationEntity
from controller.auth import jwt_handler
from controller.email import email

userRouter = APIRouter()
db = conn.sight.user


# @userRouter.get('/auth/authenticate')
# async def authenticate(token: str = Depends(oauth2_scheme)):
#     return {"token": token}


@userRouter.post('/user/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if checkUser(form_data):
        return {"access_token": jwt_handler.signJWT(form_data.username), "token_type": "bearer"}
    else:
        return {"access_token": None, "detail": "Invalid Credentials"}


@userRouter.get('/user/authenticate/{token}')
async def authenticate(token: str):
    return {"token": jwt_handler.decodeJWT(token)}


@userRouter.get('/user/details/{token}')
async def getUserDetails(token: str):
    auth = jwt_handler.decodeJWT(token)
    if (auth == {} or auth == None):
        return None
    else:
        user = db.find_one({"username": auth['userID']})
        return {"name": user['name'], "username": user['username']}


@userRouter.post('/user/register')
async def create_user(user: User):
    # jwt_handler.authenticate()
    checkUser = db.find_one({'username': user.username})
    if checkUser is not None:
        return {"token": None, "msj": 'User already exist!'}
    db.insert_one(dict(user))

    return jwt_handler.signJWT(user.username)
    # return usersEntity(db.find())
    # return res


# @userRouter.post('/send/email')
# async def send_email():
#     email.sendEmail("hissey@getnada.com", "Test", "Hello")


def checkUser(data: UserLogin):
    if (userData := db.find_one({"username": data.username, "password": data.password})) is not None:
        return userData
