## 总览
该项目用来存储文件，我预计将它和我的树莓派以及FRPS一起搭配，作为图床使用。因为我不想买对象存储服务，所以用了一点点时间做了这个项目。

## 如何使用
这个项目是基于Python3的，所以你首先要有Python环境, 然后运行`pip3 install -r requirements.txt`来安装依赖。

你可以通过`uvicorn main:app`来运行项目，当然你也可以使用`gunicorn`，但是这个项目的目的就是给个人使用的，所以我觉得`uvicorn`就足够了。
默认会暴露端口在`http://localhost:8000`，web页面也在这里面。

默认的用户名和密码是`example`。
你可以在`config.py`中编辑配置。