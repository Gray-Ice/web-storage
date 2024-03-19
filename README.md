## Overview
[简体中文](https://github.com/Gray-Ice/web-storage/blob/main/zh_README.md)
This project is for storage and manage your file. I would like to use it with FRP. It's for store files, because I don't want to buy Object Storage service, so I use it.

## How to Use it
This project is based on Python3, so you need have python environment first, and then you should install dependencies with `pip3 install -r requirements.txt`.

To start the project, you can run command: `uvicorn main:app` or use `gunicorn`, it will expose a port default on `http://localhost:8000`.

You can visit the web page default in http://localhost:8000, it's quite simple, but you can use it, and it works :\(

To use it, you need login first. Default username and password both are `example`.

You can modify the configuration file at `config.py`. I've not considered multiple user mode now.

## TODO List
 - [ ] File access control
- [ ] Delete file
