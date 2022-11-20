#! /usr/bin/env python3

from Crypto.Util.number import long_to_bytes
from copy import deepcopy

len_m0 = 62
B = 2**(len_m0*8)

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

def Binary_search(si, id, a, b, N):
    a = id*B+a
    b = id*B+b

    # возможные границы для значения r
    r_left = (si*a+1-(id+1)*B)//N
    r_right = (si*b-id*B)//N
    if (r_right-r_left != 1):
        print("Error!:")
        inp = input("exit")
    
    r = r_right

    aa = (id*B + r*N)//si
    bb = ((id+1)*B - 1 + r*N)//si+1
    #пересекаем найденный интервал с интервалом [a,b]
    newa = max(a,aa) & (B-1)
    newb = min(b,bb) & (B-1)

    return (newa,newb)


def main():
    f = open("output.txt", 'r')
    N = int(f.readline().strip().split(" ")[2],16)
    f.readline()
    # запросы к оракулу
    reqs = [[int(i,16) for i in  f.readline().strip().split(",")] for _ in range(2)]
    f.readline()
    f.readline()
    f.readline()
    # запросы к оракулу при "бинарном поиске"
    bin_reqs = []
    for line in f.readlines():
        bin_reqs.append([int(i,16) for i in  line.strip().split(",")])
    
    intervals = [(0,B-1)]
    for (id, si) in reqs:
        tmp_intervals = []
        for (a,b) in intervals:
            for (c,d) in Narrowing_interval(si, id, a, b, N):
                # при формировании интервала убираем байт паддинга
                (c,d) = (c & (B-1), d & (B-1))
                if (c,d) not in tmp_intervals:
                    tmp_intervals.append((c,d))
        intervals = deepcopy(tmp_intervals)

    if (len(intervals) != 1):
        print("Error!!!")
        return

    (a,b) = intervals[0]
    for (id, si) in bin_reqs:
        (a,b) = Binary_search(si, id, a, b, N)

    print(long_to_bytes(b>>(30*8)))


if __name__ == '__main__':
    main()