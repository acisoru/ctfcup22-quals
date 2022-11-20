#! /usr/bin/env python3

from pylfsr import LFSR
from Crypto.Util.number import long_to_bytes
from base64 import b64encode
import json

f = [0,0,0,1,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,1,1,0,1,1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,0,0,0,1,1,1,1,0,1,1,1]
pickup_points = [7, 10, 17, 23, 36, 42]
poly = [48, 47, 44, 42, 41, 37, 36, 35, 31, 30, 27, 24, 23, 21, 20, 17, 16, 15, 13, 10, 9, 8, 7, 4, 3, 1]
start_pos = 1000
N = 20000


def Gen_gamma_filt_gen(state, N):
    L = LFSR(fpoly=poly,initstate = state)

    gamma = []
    L.runKCycle(start_pos)
    for _ in range(N):
        st = list(L.state)
        st.reverse()
        bin_idx = [st[i] for i in pickup_points]
        idx = int("".join([str(i) for i in bin_idx]),2)
        gamma.append(f[idx])
        L.runKCycle(1)

    return gamma


def Dump_gamma(gamma, filename):
    dict = {"g": gamma}
    filename = f"{filename}.json"
    with open(filename, 'w') as file_object:
        json.dump(dict, file_object)


def main():
    init_state = 48*[0]
    print("0b"+"".join([str(i) for i in init_state]))

    bt = long_to_bytes(int("".join([str(i) for i in init_state]),2))
    flag = b64encode(bt).decode()
    print("CUP{"+flag+"}")

    g = Gen_gamma_filt_gen(init_state, N)
    filename = "output"

    Dump_gamma(g, filename)


if __name__ == "__main__":
    main()