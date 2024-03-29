import shutil

from fastapi import APIRouter, UploadFile, Form, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import typing
from typing_extensions import Annotated
import os
from utils import check_token
from config import ROOT_FOLDER

router = APIRouter(prefix="/files", dependencies=[Depends(check_token)])


class _GetFileModel(BaseModel):
    root: str = "/"


class _ReturnFilesModel(BaseModel):
    dirs: typing.List[str]


@router.get("/get_files")
async def get_files(root: str = "/"):
    if not root.endswith("/"):
        root = f"{root}/"
    folders = os.listdir(f"{ROOT_FOLDER}{root}")
    return_data = []
    for folder in folders:
        is_dir = False
        full_path = f"{ROOT_FOLDER}{root}{folder}"
        print(full_path)
        if os.path.isdir(full_path):
            is_dir = True
        size = os.stat(full_path).st_size
        return_data.append({"name": folder, "dir": is_dir, "path": full_path, "size": size})

    return JSONResponse(status_code=200, content={"dirs": return_data, "root": root})


@router.post("/upload_file")
async def upload_file(file: UploadFile, path: Annotated[str, Form()] = "/", name: Annotated[str, Form()] = ""):
    if name == "":
        filename = file.filename
    else:
        filename = name
    path = f"{ROOT_FOLDER}{path}"
    if path.startswith("/web/"):
        return JSONResponse(status_code=500, content={"You can't upload files to this path."})
    if not os.path.exists(path):
        return JSONResponse(status_code=500, content={"msg": f"can not find path: {path}"})
    if not path.endswith("/"):
        path = f"{path}/"
    with open(f"{path}{filename}", "wb") as f:
        f.write(await file.read())
    return JSONResponse(status_code=200, content={"msg": f"{path}{filename} already created"})


class _DeleteFileModel(BaseModel):
    path: str


@router.post("/delete")
async def delete_file(model: _DeleteFileModel):
    if not os.path.exists(model.path):
        return JSONResponse(status_code=500, content={"msg": f"Can not found path {model.path}"})
    if os.path.isdir(model.path):
        shutil.rmtree(model.path)
        return JSONResponse(status_code=200, content={"msg": f"remove folder {model.path} success"})
    os.remove(model.path)
    return JSONResponse(status_code=200, content={"msg": f"removed path {model.path}."})