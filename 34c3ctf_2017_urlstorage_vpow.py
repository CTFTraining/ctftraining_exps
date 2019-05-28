#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    Author : Virink <virink@outlook.com>
    Date   : 2019/05/28, 15:27
"""


import sys
import random
import string
import struct
from hashlib import sha256

PROOF_OF_WORK_HARDNESS = 13371337


def proof_of_work_okay(chall, solution):
    hardness, chall = chall.split("_")
    h = sha256(chall.encode('ASCII') +
               struct.pack('<Q', solution)).hexdigest()
    return int(h, 16) < 2**256 / int(hardness)


def random_string(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def solve_proof_of_work(task):
    ''' You can use this to solve the proof of work. '''
    print('Creating proof of work for {}'.format(task))
    i = 0
    while True:
        if i % 1000000 == 0:
            print('Progress: %d' % i)
        if proof_of_work_okay(task, i):
            print('Solution: {}'.format(i))
            return i
        i += 1
    raise ValueError('could not create proof of work')


if __name__ == '__main__':
    if sys.version[0] == '2':
        input = raw_input
    if len(sys.argv) < 2:
        print("Usage : %s challenge" % sys.argv[0])
    else:
        if sys.argv[1] == 'ask':
            challenge = random_string()
            print('Proof of work challenge: {}'.format(challenge))
            sol = int(input('Your response? '))
            if not proof_of_work_okay(challenge, sol):
                print('Wrong :(')
                exit(1)
        elif sys.argv[1] == 'v':
            challenge = input("challenge : ")
            print('Proof of work challenge: {}'.format(challenge))
            sol = int(input('Your response? '))
            if not proof_of_work_okay(challenge, sol):
                print('Wrong :(')
                exit(1)
            else:
                print("Good Job")
        else:
            print(solve_proof_of_work(sys.argv[1]))
