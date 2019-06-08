#!/usr/bin/env python2
# -*- coding:utf-8 -*-
"""
    Author : blus
"""

import os
import hashlib

from pwn import *

context.log_level = "debug"
dic = "0123456789abcdef"


def burst(hash1, pre2):
    for i1 in range(0, 256):
        for i2 in range(0, 256):
            for i3 in range(0, 256):
                s1 = pre2+chr(i1)+chr(i2)+chr(i3)
                s2 = hashlib.sha256(s1).hexdigest()
                if str(s2) == hash1:
                    print s1.encode('hex')
                    return s1.encode('hex')
                    break


if __name__ == "__main__":
    # Connect
    s = remote("127.0.0.1", 10000)
    s1 = s.recvline()
    s2 = s.recvline()
    s3 = s.recvline()
    hash1 = s2[35:-1]
    pre = s3[26:-1]
    pre2 = pre.decode('hex')
    # Proof
    print "[+] start proof..."
    s3 = burst(hash1, pre2)
    s.sendline(s3)

    m1 = 'FLAG{2^8rsa7589693fc689c77c5f5262d654272427}'.encode('hex')
    s.recvuntil('long_to_bytes(m).encode(\'hex\')=')
    s.sendline(m1)

    s.recvuntil('long_to_bytes(m).encode(\'hex\')=')
    m2 = 'FLAG{2^8rsa6e277f355dbe6da3edd6f356d2db6d6f}'.encode('hex')
    s.sendline(m2)

    s.recvuntil('long_to_bytes(m).encode(\'hex\')=')
    m3 = 'FLAG{2^8rsa5ab086745f6ec745619a8b65fe4ec560}'.encode('hex')
    s.sendline(m3)

    s.recvuntil('long_to_bytes(m).encode(\'hex\')=')
    m4 = 'FLAG{2^8rsa5ab086745f6ec745619a8b65fe4ec560}'.encode('hex')
    s.sendline(m4)

    s.recvuntil('long_to_bytes(m).encode(\'hex\')=')
    m5 = 'FLAG{2^8rsa398cf8df7c26661bb7cb65b2b9fae25e}'.encode('hex')
    s.sendline(m5)

    s.recvuntil('long_to_bytes(m).encode(\'hex\')=')

    m6 = "6b3bb0cdc72a7f2ce89902e19db0fb2c0514c76874b2ca4113b86e6dc128d44cc859283db4ca8b0b5d9ee35032aec8cc8bb96e8c11547915fc9ef05aa2d72b28"
    s.sendline(m6)

    s.interactive()
