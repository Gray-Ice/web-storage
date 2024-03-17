from jose import jwt, JWTError
import typing
import config
from datetime import datetime


def decode_token(token: str) -> typing.Union[None, dict]:
    try:
        return jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
    except JWTError:
        return None


def gen_token(data: dict, expire: datetime):
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt
