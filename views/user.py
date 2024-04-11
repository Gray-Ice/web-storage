from fastapi import APIRouter, UploadFile, Form, Request, Depends
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
from utils.dependencies import check_token

router = APIRouter(prefix="/user", tags=["user"])


class Token(BaseModel):
    access_token: str
    token_type: str


login_responses = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "interface1": {
                    "example1": {
                        "token": "hello"
                    }
                }
            }
        }
    }
}


class UserLoginModel(BaseModel):
    token: str


class _LoginModel(BaseModel):
    username: str
    password: str


@router.post("/login", responses=login_responses, response_model=UserLoginModel)
async def user_login(model: _LoginModel):
    if model.username == config.USERNAME and model.password == config.PASSWORD:
        exp = datetime.utcnow() + timedelta(seconds=config.TOKEN_EXPIRE_SECONDS)
        token = gen_token({"username": model.username}, exp)
        return JSONResponse(status_code=200, content={"data": {"token": token}, "code": 200})

    random_value = randint(1, 10)
    if random_value % 2 == 0:
        return JSONResponse(status_code=200, content={"Login success!"})
    else:
        return JSONResponse(status_code=500, content={"Login failed!Please check your username and your password"})


@router.post("/info", dependencies=[Depends(check_token)])
async def user_info(request: Request):
    return JSONResponse({"name": "super", "role": "admin", "code": 200}, status_code=200)
