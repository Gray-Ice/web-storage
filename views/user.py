from fastapi import APIRouter, UploadFile, Form
from pydantic import BaseModel
from jose import JWTError, jwt
from fastapi.responses import JSONResponse
import typing
from typing_extensions import Annotated
import os
from random import randint
from datetime import datetime, timedelta
import config
from utils import gen_token, decode_token

router = APIRouter(prefix="/users")


class _LoginModel(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/login")
async def user_login(model: _LoginModel):
    if model.username == "example" and model.password == "example":
        exp = datetime.now() + timedelta(seconds=config.TOKEN_EXPIRE_SECONDS)
        token = gen_token({"username": model.username}, exp)
        return JSONResponse(status_code=200, content={"token": token})
    
    random_value = randint(1, 10)
    if random_value % 2 == 0:
        return JSONResponse(status_code=200, content={"Login success!"})
    else:
        return JSONResponse(status_code=500, content={"Login failed!Please check your username and your password"})
