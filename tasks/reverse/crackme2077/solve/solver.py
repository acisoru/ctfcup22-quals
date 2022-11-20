from subprocess import Popen, PIPE, STDOUT
import string
import time

BINARY = "Crackme2077.exe"

def get_delta(data):
    cnt = 0

    p = Popen([BINARY], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    
    start = time.time()
    out = p.communicate(input=data)[0]
    end = time.time()
    return end-start

# find size of flag
# get initial inst count
init = get_delta(b"aaa")
print("[+] init value: {}".format(init))
payload_size = 0

for i in range(1, 32):
    tmp = get_delta(b'CUP{' + b'a' * i + b'}')
    print('{} : {}'.format(i, tmp))

    if (tmp - init) > 0.1:
        payload_size = i
        print("Looks strange:", i, tmp, init)
        init = tmp
        break

alph = string.digits + "_" + string.ascii_letters
cur_flag = b"CUP{"
payload_size -= (len(cur_flag)-4)
init = get_delta(cur_flag + bytes(b"a" * (payload_size)+ b"}"))

for i in range(0, payload_size):
    for j in alph:
        payload = cur_flag + bytes([ord(j)]) + b"a" * (payload_size-i-1)+ b"}"
        tmp = get_delta(payload)
        print(j, tmp, payload)
        if (tmp - init) > 0.23:
            print("Looks strange:", i, tmp, init)
            cur_flag += bytes([ord(j)])
            print("Current flag guess: {}".format(cur_flag + b"}"))
            init = tmp
            break