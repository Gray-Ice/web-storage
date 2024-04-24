## Overview
[简体中文](https://github.com/Gray-Ice/web-storage/blob/main/zh_README.md)
This project is for storage and manage your file. I would like to use it with FRP. It's for store files, because I don't want to buy Object Storage service, so I use it.
It has a frontend here: [web-storage-frontend](https://github.com/Gray-Ice/web-storage-frontend). 
I don't suggest you use it now, because I will keep update it, and at one day, you can simply use with in docker.
## How to Use it
I don't suggest you deployment this project at this time.
This project is based on Python3, so you need have python environment first, and then you should install dependencies with `pip3 install -r requirements.txt`.

To start the project, you can run command: `uvicorn main:app` or use `gunicorn`, it will expose a port default on `http://localhost:8000`.

To use it, you need login first. Default username and password both are `example`.

You can modify the configuration file at `config.py`. I've not considered multiple user mode now.

## TODO List
 - [ ] File access control
 - [ ] Delete file
- [ ] Modify already existing Markdown 
