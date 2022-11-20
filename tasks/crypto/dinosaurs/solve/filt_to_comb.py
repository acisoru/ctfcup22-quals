#! /usr/bin/env python3

from pylfsr import LFSR
import random

f = [0,0,0,1,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,1,1,0,1,1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,0,0,0,1,1,1,1,0,1,1,1]
pickup_points = [7, 10, 17, 23, 36, 42]
poly = [48, 47, 44, 42, 41, 37, 36, 35, 31, 30, 27, 24, 23, 21, 20, 17, 16, 15, 13, 10, 9, 8, 7, 4, 3, 1]
start_pos = 1000


def Gen_gamma_comb_gen(state, N):
    LFSRS = [LFSR(fpoly=poly,initstate = state) for _ in range(6)]
    
    seq = []
    for i, L in enumerate(LFSRS):
        L.runKCycle(pickup_points[i])
        L.runKCycle(start_pos)
        L.runKCycle(N)
        seq.append(list(L.seq[pickup_points[i]+start_pos:]))

    idxs = []
    for i in range(N):
        tmp_idx = []
        for s in seq:
            tmp_idx.append(s[i])
        idxs.append(tmp_idx)

    gamma = []
    for bin_idx in idxs:
        idx = int("".join([str(i) for i in bin_idx]),2)
        gamma.append(f[idx])
    
    return gamma

def Gen_gamma_filt_gen(state, N):
    L = LFSR(fpoly=poly,initstate = state)

    gamma = []
    L.runKCycle(start_pos)
    for _ in range(N):
        state = list(L.state)
        state.reverse()
        bin_idx = [state[i] for i in pickup_points]
        idx = int("".join([str(i) for i in bin_idx]),2)
        gamma.append(f[idx])
        L.runKCycle(1)

    return gamma


def main():
    init_state = [random.randint(0,1) for _ in range(48)]
    init_state.reverse()
    N = 1000
    g1 = Gen_gamma_comb_gen(init_state, N)
    g2 = Gen_gamma_filt_gen(init_state, N)
    print(g1==g2)


if __name__ == "__main__":
    main()