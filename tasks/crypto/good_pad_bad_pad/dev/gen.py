from Crypto.Util.number import bytes_to_long, long_to_bytes
from copy import deepcopy
import random

random1 = long_to_bytes(0xeed4adb47cc8ad83a6b6aec647d4f41a5b457e644b42384c1819008b91cb)
message = b'CUP{Bl3ICheNbaChEr_St1lL_AlIVE!}'
len_m0 = len(random1)+len(message)
B = 2**(len_m0*8)

random.seed()

#def Get_param(bitlen):
#    p = random_prime(2^(bitlen//2)-1,False,2^(bitlen//2-1))
#    while not ZZ((p-1)/2).is_prime():
#        p = random_prime(2^(bitlen//2)-1,False,2^(bitlen//2-1))
#    q = random_prime(2^(bitlen//2)-1,False,2^(bitlen//2-1))
#    while not ZZ((q-1)/2).is_prime():
#        q = random_prime(2^(bitlen//2)-1,False,2^(bitlen//2-1))
#    
#    e = 65537
#    d = inverse_mod(e,(p-1)*(q-1))
#    N = p*q
#    return N,e,d


# msg должно иметь длину 62 байта
def PKCS(id,msg,e,N):
    m = bytes_to_long(id+msg)
    return pow(m,e,N)


def Check_si(si,id,m0,N):
    id_int = bytes_to_long(id)
    msg = bytes_to_long(id+m0)
    if ((si*msg%N) >> len_m0*8) == id_int:
        return True
    return False


def Get_s(s0,id,m0,N):
    s = s0
    while not Check_si(s,id,m0,N):
        s += 1
    return s


def Narrowing_interval(si, id, a, b, N):
    a = id*B+a
    b = id*B+b

    newM = []  # собираем новые интервалы в этот массив
    #перебираем все подходящие значения для r
    for r in range((a*si - (id+1)*B + 1)//N,
                  ((b*si - id*B)//N + 1)):
        #рассчитываем границы aa и bb для нового интервала m0, опираясь на текущее r
        aa = (id*B + r*N)//si
        bb = ((id+1)*B - 1 + r*N)//si+1
        #пересекаем найденный интервал  с интервалом [a,b]
        newa = max(a,aa)		                       
        newb = min(b,bb)		                     
        if newa <= newb:		                        
            newM.append((newa, newb))

    return newM


def Binary_search(si, m0, a, b, N):
    id_int = random.randrange(1,255)
    id = bytes([id_int])
    si = Get_s(si,id,m0,N)
    a = id_int*B+a
    b = id_int*B+b

    r = ((b*si - id_int*B)*2)//N # начальное значение для r
    s_new = 0
    
    found = False	
    while not found:
        for s in range((id_int*B + r * N)//b,((id_int+1)*B-1 + r * N)//a+1):
            if Check_si(s,id,m0,N):
                found = True
                s_new = s
                break # мы нашли si
        if not found:
            r  += 1   # пытаемся попробовать следующее значение для r


    aa = (id_int*B + r*N)//s_new
    bb = ((id_int+1)*B - 1 + r*N)//s_new+1
    #пересекаем найденный интервал с интервалом [a,b]
    newa = max(a,aa) & (B-1)
    newb = min(b,bb) & (B-1)
    
    # запечатляем нужную инфу для таски
    print(f"{hex(id_int)},{hex(s_new)}")

    return (newa,newb), s_new


def main():
    #N,e,d = Get_param(512)
    #print("N = ",hex(N))
    #print("e = ",hex(e))
    #print("d = ",hex(d))

    N =  0x62bd979b83e7d542d5a77a05733d0f213a41f44c67b93097b5f93bbefb5b38ad6ac1be2b42d925d704d9d51bd2e15be1a78b266b5e9bd5bdc7896a351dc42f2d
    print(f"N = {hex(N)}")
    m0 = message+random1

    req = []
    for id_int in [3,7,9,11,15]:
        id = bytes([id_int])
        s0 = N//((id_int+1)*B)<<16
        for _ in range(1):
            s = Get_s(s0,id,m0,N)
            s0 = s+1
            req.append((id_int, s))

    print(f"id,s:")
    # решаем таск, на входе имеем req, N, e
    intervals = [(0,B-1)]
    for (id, si) in req:
        print(f"{hex(id)},{hex(si)}")
        tmp_intervals = []
        for (a,b) in intervals:
            for (c,d) in Narrowing_interval(si, id, a, b, N):
                # при формировании интервала убираем байт паддинга
                (c,d) = (c & (B-1), d & (B-1))
                if (c,d) not in tmp_intervals:
                    tmp_intervals.append((c,d))

        intervals = deepcopy(tmp_intervals)
        if (len(intervals) == 1):
            break
    
    if (len(intervals) != 1):
        print("Error!!!")
        return

    print("start binary search")
    print("have id and s_i, calc s_{i+1}")
    print("id,s_{i+1}:")
    
    (a,b) = intervals[0]
    si = N//B<<16
    # нам не интересны биты рандома, поэтому как только биты флага зафиксированы, выходим
    while ((len(bin(b-a))-2)>len(random1)*8):
        (a,b), si = Binary_search(si, m0, a, b, N)


if __name__ == '__main__':
    main()