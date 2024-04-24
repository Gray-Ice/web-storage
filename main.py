from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware

import config
from views.files import router as file_router
from views.user import router as user_router
from views.notes import router as notes_router

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True)
app.include_router(file_router)
app.include_router(user_router)
app.include_router(notes_router)


app.mount("/static", StaticFiles(directory=config.ROOT_FOLDER), name="static")
app.mount("/web", StaticFiles(directory="web"), name="web")

@app.get("/uploadfile")
async def upload_file():
    return JSONResponse(status_code=200, content={"msg": "starting project"})

@app.get("/")
async def index():
    with open("./web/index.html", "r", encoding="utf-8") as f:
        html = f.read()
    headers = {"Content-Type": "text/html"}
    response = Response(status_code=200, content=html, headers=headers)
    return response
