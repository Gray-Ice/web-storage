import shutil

from fastapi import APIRouter, UploadFile, Form, Depends, Request, Query, Response
from pydantic import BaseModel, Field
from datetime import datetime
from fastapi.responses import JSONResponse, FileResponse
import typing
from typing_extensions import Annotated
import os

import config
from utils import check_token
from config import ROOT_FOLDER, NOTE_PATH

router = APIRouter(prefix="/notes")


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


@router.get("/get_notes", response_model=_ReturnFilesModel, dependencies=[Depends(check_token)])
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
        return_data.append({"name": file, "dir": is_dir, "path": f"{root}{file}", "size": size})

    return JSONResponse(status_code=200, content={"dirs": return_data, "root": root, "code": 200})


class _DeleteFileModel(BaseModel):
    path: str


@router.post("/delete", dependencies=[Depends(check_token)])
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
    back_with_text: bool


class NormalResponse(BaseModel):
    code: int
    msg: str


class CheckNoteExistsResponse(NormalResponse):
    text: typing.Optional[str] = None
    path: typing.Optional[str] = None


@router.get("/check_note_exists", response_model=CheckNoteExistsResponse, dependencies=[Depends(check_token)])
async def check_note_exists(date: str,
                            filename: str,
                            get_text: bool):
    try:
        dt = datetime.fromisoformat(date)
    except ValueError:
        return CheckNoteExistsResponse(code=500, msg=f"can not recognize your date: {date}")

    path = get_path_by_str_date(dt)
    if not filename.endswith(".md"):
        print("Adding")
        file_path = f"{path}/{filename}.md"
    else:
        file_path = f"{path}/{filename}"

    merged_file_path = f"{NOTE_PATH}{file_path}"
    if os.path.exists(merged_file_path):
        if get_text:
            with open(merged_file_path, encoding="utf-8") as f:
                text = f.read()
            return CheckNoteExistsResponse(code=202, text=f"{text}", msg="", path=path)
        return CheckNoteExistsResponse(code=200, msg=f"{merged_file_path} already exists")
    return CheckNoteExistsResponse(code=404, msg=f"{merged_file_path} is not exists")


class UploadNoteSuccessResponse(NormalResponse):
    path: str


class UploadNoteFailedResponse(NormalResponse):
    text: str = None
    path: str = None


@router.post("/upload_note", response_model=NormalResponse | UploadNoteSuccessResponse | UploadNoteFailedResponse, dependencies=[Depends(check_token)])
async def upload_note(model: UploadNotesRequest):
    try:
        dt = datetime.fromisoformat(model.date)
    except ValueError:
        return UploadNoteFailedResponse(code=500, msg=f"can not recognize your date: {model.date}", )
    path = get_path_by_str_date(dt)
    if not path.endswith("/"):
        path += "/"
    folder_path = f"{NOTE_PATH}{path}"
    file_path = f"{NOTE_PATH}{path}{model.filename}.md"

    # Check if we need overwrite the file
    if os.path.exists(file_path):
        if model.back_with_text:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            print("Reading")
            return UploadNoteFailedResponse(code=202, msg="file is already exists", text=text)

        if not model.overwrite:
            return UploadNoteFailedResponse(code=500, msg="file is already exists", )
            # return JSONResponse("file is already exists", 200)

    if not os.path.exists(file_path):
        os.makedirs(folder_path, exist_ok=True)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(model.text)
    except Exception as e:
        return UploadNoteFailedResponse(code=500, msg=f'{type(e)}--{e}')

    return UploadNoteSuccessResponse(code=200, msg=f"upload note success", path=path)


class UploadFileResponse(NormalResponse):
    path: str = None


@router.post("/upload_file", dependencies=[Depends(check_token)])
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
    if not path.endswith("/"):
        path = f"{path}/"
    merged_path = f"{NOTE_PATH}{path}"
    if not os.path.exists(merged_path):
        if file.filename.endswith(".jpg") or file.filename.endswith(".png") or file.filename.endswith(".svg"):
            merged_path = f"{merged_path}/images/"
            os.makedirs(merged_path, exist_ok=True)
        else:
            return UploadFileResponse(code=200, msg=f"can not find path: {merged_path}")
            # return JSONResponse(status_code=200, content={"msg": f"can not find path: {path}", "code": 500})
    with open(f"{merged_path}{filename}", "wb") as f:
        f.write(await file.read())
    return UploadFileResponse(code=200,
                              msg=f"{path}{filename} already created",
                              path=f"/notes/get_file?path={path}{filename}"
                              )
    # return JSONResponse(status_code=200, content={"msg": f"{path}{filename} already created", "code": 200})


@router.get("/get_file")
async def get_file(path: str = Query(description="File path")):
    path_folders = path.split("/")
    print(path_folders)
    if not path.startswith("/"):
        return Response(status_code=404)
    if len(path_folders) < 2:
        return Response(status_code=404)

    full_path = f"{NOTE_PATH}{path}"
    print(full_path)
    if not os.path.exists(full_path):
        print("Unexist")
        return Response(status_code=404)

    return FileResponse(path=full_path, )

