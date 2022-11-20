#! /usr/bin/env python3

import random
import json
from Crypto.Util.number import bytes_to_long


# то, что происходит внутри смарт-карты --------------------------------

def MontMulTime(a, b, n, r, n_inverse, time):
    t = a*b
    m = t*n_inverse & (r-1)
    u = (t+m*n)//r
    # 3 умножения и одно деление за 3 цикла + сложение и взятие нижних бит
    # каждый процессорный тик стоит 250 временных единиц
    time += (3*4+2*1)*250

    extra = 0
    if(u > n):
        extra = 1
        time += 250
        u = u - n
    return u, time, extra


def MontExp(message, n, exp):
    time = 0
    message, time, extra = MontMulTime(message, r_square, n, r, n_inverse, time)
    current, time, extra = MontMulTime(message, message, n, r, n_inverse, time)
    for j in range(1, len(exp)-1):
        if exp[j] == "1":
            current, time, extra = MontMulTime(current, message, n, r, n_inverse, time)
        current, time, extra = MontMulTime(current, current, n , r, n_inverse, time)
    if exp[-1] == "1":
        current, time, extra = MontMulTime(current, message, n, r, n_inverse, time)
    current, time, extra = MontMulTime(current, 1, n , r, n_inverse, time)
    return current, time

#----------------------------------------------------------


def Generate_messages_and_time(amount, n, filename):
    M = []
    time = []
    for i in range(amount):
        m = random.getrandbits(len(bin(n))-2)
        while m > n :
            m = random.getrandbits(len(bin(n))-2)
        M.append(m)
        res = MontExp(m, n, secret)
        time.append(res[1])

    dict = {"m": M, "t": time}
    filename = f"{filename}.json"
    with open(filename, 'w') as file_object:
        json.dump(dict, file_object)


def Gen_n_and_d(pbits=512, len=21):
    p = 0
    q = 0
    while True:
        p = random_prime(2^pbits-1, false, 2^(pbits-1))
        if ZZ((p-1)/2).is_prime():
            break
    while True:
        q = random_prime(2^pbits-1, false, 2^(pbits-1))
        if ZZ((q-1)/2).is_prime():
            break
    d = random_prime(2^(len*8)-1, false, 2^(len*8-1))
    
    n = p*q
    return n, d


def main():
    sampleSize = 12000
    filename = "output"
    n, d = Gen_n_and_d()
    print(f"n = {hex(n)}")

    global secret
    secret = bin(d)[2:]

    # переменные, необходимые для умножения Монтгомери
    # эти константы могут быть вычислены один раз для всех дальнейших возведений в степень
    global r
    r = (int)(pow(2, len(bin(n)[2:])))
    global n_inverse
    n_inverse = (int)(pow(-n,-1,r))
    global r_square
    r_square = (int)(pow(r,2,n))
    
    Generate_messages_and_time(sampleSize, n, filename)

    #флаг без CUP{}
    flag = "*********************"
    enc_flag = bytes_to_long(flag)^d
    print(f"enc_flag = {hex(enc_flag)}")


if __name__ == "__main__":
    main()