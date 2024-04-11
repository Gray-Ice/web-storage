from fastapi import HTTPException, Header
from utils.token import decode_token
import typing


def check_token(authorization: typing.Annotated[str, Header()] = ""):
    if not authorization:
        raise HTTPException(status_code=401, detail={"msg": "You must login before request this resource."})
    try:
        header, token = authorization.split(" ")
        print(f"The header is {header}, and the token is {token}")
    except ValueError:
        print(authorization)
        return HTTPException(401, {"msg": "You must login before request this resource"})
    token = decode_token(token)
    if token is None:
        raise HTTPException(status_code=401, detail={"msg": "You must login before request this resource."})
    print(f"This is token: {token}")
    return token
