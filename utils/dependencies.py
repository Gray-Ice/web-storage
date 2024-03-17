from fastapi import HTTPException, Header
from utils.token import decode_token
import typing


def check_token(token: typing.Annotated[str, Header()] = ""):
    if not token:
        raise HTTPException(status_code=401, detail={"msg": "You must login before request this resource."})
    token = decode_token(token)
    if token is None:
        raise HTTPException(status_code=401, detail={"msg": "You must login before request this resource."})
    return token
