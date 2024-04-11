SECRET_KEY = "example"
ALGORITHM = "HS256"
ROOT_FOLDER = "static"

TOKEN_EXPIRE_SECONDS = 60 * 60 * 24 * 30
# TOKEN_EXPIRE_SECONDS = 30

USERNAME = "example"
PASSWORD = "example"

BACKEND_PATH = "http://localhost:8000"

def init():
    # with open("./web/base.js", "r", encoding="utf-8") as f:
    #     f.readline()
    #     backend_url_config = f'window.host = "{BACKEND_PATH}"'
    #     data = f.read()
    #     data = f"{backend_url_config}\n{data}"
    #
    # print(data)
    # with open("./web/base.js", "w", encoding="utf-8") as f:
    #     f.write(data)
    pass

init()
