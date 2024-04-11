import shutil

from fastapi import APIRouter, UploadFile, Form, Depends, Request
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
    root: str


@router.get("/get_files", response_model=_ReturnFilesModel)
async def get_files(root: str = "/"):
    """
    Get the files under root path
    :param root: folder path
    """
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

    return JSONResponse(status_code=200, content={"dirs": return_data, "root": root, "code": 200})


# class UploadFileModel(BaseModel):
#     path: str = "/"
#     name: str = ""
@router.post("/upload_file")
async def upload_file(file: UploadFile, path: Annotated[str, Form()] = "/", name: Annotated[str, Form()] = ""):
    """
    Upload file under path, and rename it to name if name was specified
    :param file: The file
    :param path: the path that you want transport file into
    :param name: if you specified the name,
     the file will be renamed to name, or it will use the default file name already belongs the file
    """
    print(f"The root path is {path}")
    if name == "":
        filename = file.filename
    else:
        filename = name
    path = f"{ROOT_FOLDER}{path}"
    if path.startswith("/web/"):
        return JSONResponse(status_code=500, content={"msg": "You can't upload files to this path.", "code": 500})
    if not os.path.exists(path):
        return JSONResponse(status_code=500, content={"msg": f"can not find path: {path}", "code": 500})
    if not path.endswith("/"):
        path = f"{path}/"
    with open(f"{path}{filename}", "wb") as f:
        f.write(await file.read())
    return JSONResponse(status_code=200, content={"msg": f"{path}{filename} already created", "code": 200})


class _DeleteFileModel(BaseModel):
    path: str


@router.post("/delete")
async def delete_file(model: _DeleteFileModel):
    """
    Delete the file that pointed to by the path
    """
    if not os.path.exists(model.path):
        return JSONResponse(status_code=500, content={"msg": f"Can not found path {model.path}"})
    if os.path.isdir(model.path):
        shutil.rmtree(model.path)
        return JSONResponse(status_code=200, content={"msg": f"remove folder {model.path} success"})
    os.remove(model.path)
    return JSONResponse(status_code=200, content={"msg": f"removed path {model.path}."})
