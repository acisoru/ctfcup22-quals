#!/usr/bin/env python3

from pwn import *
from hashlib import sha256
from base64 import b64encode
import sys

def calc_pow(prefix, correct):
    for i in range(0, 10000000000000):
        if sha256(prefix.encode() + str(i).encode()).hexdigest()[:6] == correct:
            return str(i).encode()

if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("{-} Usage: python3 sploit_loader.py <host> <port> <link>")
        sys.exit(0)

    host = sys.argv[1]
    port = sys.argv[2]
    link = sys.argv[3]

    r = remote(host, port)

    buf = r.recvuntil("W: ").split(b'\n')
    prefix = buf[0].split(b': ')[1].decode()
    correct = buf[1].split(b' == ')[1].decode()

    POW = calc_pow(prefix, correct)
    r.sendline(POW)
    r.recvuntil(b": ")
    r.sendline(link)

    r.interactive()
