import shutil

from fastapi import APIRouter, UploadFile, Form, Depends, Request
from pydantic import BaseModel, Field
from datetime import datetime
from fastapi.responses import JSONResponse
import typing
from typing_extensions import Annotated
import os

import config
from utils import check_token
from config import ROOT_FOLDER, NOTE_PATH

router = APIRouter(prefix="/notes", dependencies=[Depends(check_token)])


def get_path_by_str_date(date: datetime):
    if config.NOTE_PATH.endswith("/"):
        path = ""
    else:
        path = "/"

    path += f"{date.year}/"
    if date.month < 10:
        path += f"0{date.month}/"
    else:
        path += f"{date.month}/"
    if date.day < 10:
        path += f"0{date.day}/"
    else:
        path += f"{date.day}"
    return path


class _GetFileModel(BaseModel):
    root: str = "/"


class _ReturnFilesModel(BaseModel):
    dirs: typing.List[str]
    root: str


@router.get("/get_notes", response_model=_ReturnFilesModel)
async def get_files(root: str = "/"):
    """
    Get the files under root path
    :param root: folder path
    """
    if not root.endswith("/"):
        root = f"{root}/"
    files = os.listdir(f"{NOTE_PATH}{root}")
    return_data = []
    for file in files:
        is_dir = False
        full_path = f"{NOTE_PATH}{root}{file}"
        print(full_path)
        if os.path.isdir(full_path):
            is_dir = True
        size = os.stat(full_path).st_size
        return_data.append({"name": file, "dir": is_dir, "path": full_path, "size": size})

    return JSONResponse(status_code=200, content={"dirs": return_data, "root": root, "code": 200})


class _DeleteFileModel(BaseModel):
    path: str


@router.post("/delete")
async def delete_file(model: _DeleteFileModel):
    """
    Delete the file that pointed to by the path
    """
    path = f"{NOTE_PATH}{model.path}"
    if not os.path.exists(path):
        return JSONResponse(status_code=200, content={"msg": f"Can not found path {model.path}", "code": 500})
    if os.path.isdir(path):
        shutil.rmtree(path)
        return JSONResponse(status_code=200, content={"msg": f"remove folder {model.path} success", "code": 200})
    os.remove(path)
    return JSONResponse(status_code=200, content={"msg": f"removed path {model.path}.", "code": 200})


class UploadNotesRequest(BaseModel):
    date: str
    filename: str
    text: str
    overwrite: bool


class NormalResponse(BaseModel):
    code: int
    msg: str


class CheckNoteExistsResponse(NormalResponse):
    text: typing.Optional[str]


@router.get("/check_note_exists", response_model=CheckNoteExistsResponse)
async def check_note_exists(date: str,
                            filename: str,
                            get_text: bool):
    try:
        dt = datetime.fromisoformat(date)
    except ValueError:
        return NormalResponse(code=500, msg=f"can not recognize your date: {date}")

    path = get_path_by_str_date(dt)
    if not filename.endswith(".md"):
        print("Adding")
        file_path = f"{NOTE_PATH}/{path}/{filename}.md"
    else:
        file_path = f"{NOTE_PATH}/{path}/{filename}"

    if os.path.exists(file_path):
        if get_text:
            with open(file_path) as f:
                text = f.read()
            return CheckNoteExistsResponse(code=202, text=f"{text}", msg="")
        return NormalResponse(code=200, msg=f"{file_path} already exists")
    return NormalResponse(code=404, msg=f"{file_path} is not exists")


@router.post("/upload_note", response_model=NormalResponse)
async def upload_note(model: UploadNotesRequest):
    try:
        dt = datetime.fromisoformat(model.date)
    except ValueError:
        return NormalResponse(code=500, msg=f"can not recognize your date: {model.date}")
    path = get_path_by_str_date(dt)
    if not path.endswith("/"):
        path += "/"
    folder_path = f"{NOTE_PATH}{path}"
    file_path = f"{NOTE_PATH}{path}{model.filename}.md"

    # Check if we need overwrite the file
    if os.path.exists(file_path):
        if not model.overwrite:
            return JSONResponse("file is already exists", 500)

    if not os.path.exists(file_path):
        os.makedirs(folder_path, exist_ok=True)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(model.text)
    except Exception as e:
        return NormalResponse(code=500, msg=f'{type(e)}--{e}')

    return NormalResponse(code=200, msg="Upload note success")


@router.post("/upload_file")
async def upload_file(file: UploadFile, path: Annotated[str, Form()] = "/", name: Annotated[str, Form()] = ""):
    """
    Upload file under path, and rename it to name if name was specified
    :param file: The file
    :param path: the path that you want transport file into
    :param name: if you specified the name,
     the file will be renamed to name, or it will use the default file name already belongs the file
    """
    print(f"The root path is {path}. filename is: {file.filename}")
    if name == "":
        filename = file.filename
    else:
        filename = name
    path = f"{NOTE_PATH}{path}"
    if not os.path.exists(path):
        return JSONResponse(status_code=500, content={"msg": f"can not find path: {path}", "code": 500})
    if not path.endswith("/"):
        path = f"{path}/"
    with open(f"{path}{filename}", "wb") as f:
        f.write(await file.read())
    return JSONResponse(status_code=200, content={"msg": f"{path}{filename} already created", "code": 200})

