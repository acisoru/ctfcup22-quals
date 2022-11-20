#! /usr/bin/env python3

from pylfsr import LFSR
import numpy as np
from bisect import bisect_left
from itertools import combinations
from math import sqrt
import json
from Crypto.Util.number import long_to_bytes
from base64 import b64encode


f = [0,0,0,1,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,1,1,0,1,1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,0,0,0,1,1,1,1,0,1,1,1]
pickup_points = [7, 10, 17, 23, 36, 42]
fpoly = [48, 47, 44, 42, 41, 37, 36, 35, 31, 30, 27, 24, 23, 21, 20, 17, 16, 15, 13, 10, 9, 8, 7, 4, 3, 1]
len_reg = 48
start_pos = 1000
N = 20000


def Get_p(idx):
    bin_i = [int(bin(i)[2:].zfill(len(pickup_points))[idx]) for i in range(2**len(pickup_points))]
    return 1-sum([ i^j for i,j in zip(bin_i, f) ])/(2**len(pickup_points))


def Gen_G(poly):
    k = poly[0]
    # создаем матрицу, которая эмулирует действия регистра
    G_0 = []
    
    for i in range(k-1):
        zero_row = [0 for _ in range(k)]
        zero_row[i+1] = 1
        G_0.append(zero_row)
    
    # формируем последний ряд матрицы
    last_row = [0 for _ in range(k)]
    for i in poly:
        last_row[i-1] = 1
    last_row.reverse()
    G_0.append(last_row)

    G_0 = np.array(G_0)

    # ищем линейные соотношения для каждого из битов
    G = np.array([[0]*k for _ in range(k)])
    for i in range(k):
        G[i][i] = 1

    for i in range(start_pos):
        G = np.matmul(G,G_0)

    res_matrix = [[] for _ in G[0]]
    for i in range(N):
        for idx, elem in enumerate(G[0]):
            res_matrix[idx].append(elem%2)
        G = np.matmul(G,G_0)

    return np.array(res_matrix)
    

def Gen_lin_eq(G, k, k_prev, z, count_of_parts):
    L = len(G)

    G_columns = [G[:,i] for i in range(len(G[0]))]

    # нам необходимо добиться того, чтобы мы получили необходимые линейные соотношения
    # при минимальном количестве использованных битов гаммы.
    # Для этого мы разделим часть, которую нам нужно убрать, на отрезки
    # и будем их по очереди занулять
    step = (L-(k+k_prev))//count_of_parts

    # если шаг был последним и уже не нужно ничего изменять в линейных уравнениях
    if step == 0:
        out_mas = []
        for idx, g in enumerate(G_columns):
            g_int = int("".join([str(i) for i in g]),2)
            out_mas.append((g_int, (-1)**int(z[idx])))
        return out_mas, 1


    # подготавливаем линейные соотношения для первого шага
    lin_eqs = {}
    for idx, g in enumerate(G_columns):
        # мы будем представлять линейные комбинации в виде чисел,
        # чтобы проще было бы их сортировать потом
        g_int = int("".join([str(i) for i in g]),2)
        if g_int not in lin_eqs.keys():
            lin_eqs.update({g_int: (-1)**int(z[idx])})
        else:
            lin_eqs[g_int] += (-1)**int(z[idx])

    print(f"first, len(lin_eqs): {len(lin_eqs)}")

    for shift in range(0,L-(k+k_prev), step):
        mask = (2**step-1) << shift
        # массив для элементов с зануленной исследуемой частью
        new_lin_eqs = {}
        # массив для элементов, которые прийдется ксорить
        tmp_mas = {}
        for key in lin_eqs.keys():
            current_bits = (key & mask) >> shift
            if current_bits == 0:
                new_lin_eqs.update({key:lin_eqs[key]})
            else:
                if current_bits not in tmp_mas.keys():
                    tmp_mas.update({current_bits: [(key,lin_eqs[key])]})
                else:
                    tmp_mas[current_bits].append((key,lin_eqs[key]))

        # старый массив нам больше не нужен
        lin_eqs = new_lin_eqs.copy()

        for key in tmp_mas.keys():
            if len(tmp_mas[key]) == 1:
                continue

            for (lin_eq1, gamma1),(lin_eq2, gamma2) in combinations(tmp_mas[key],2):   
                new_gamma = abs(gamma1) * abs(gamma2) * (-1 if np.sign(gamma1) != np.sign(gamma2) else 1)
                new_lin_eq = lin_eq1 ^ lin_eq2
                if new_lin_eq not in lin_eqs.keys():
                    lin_eqs.update({new_lin_eq: new_gamma})
                else:
                    lin_eqs[new_lin_eq]+= new_gamma

        print(f"shift: {shift}, len(lin_eqs): {len(lin_eqs)}")
    
    out_mas = [(key, lin_eqs[key]) for key in lin_eqs.keys()]
    return out_mas, 2**count_of_parts


def Normalize_gamma(uniq_lin_eqs, uniq_gamma_eqs):
    res = []
    for lin_eq, gamma_eq in zip(uniq_lin_eqs, uniq_gamma_eqs):
        if np.sign(gamma_eq) != 0:
            res.append((lin_eq, np.sign(gamma_eq)))
    return res


# находим результаты линейных соотношений 
# (убираем повторы, сразу начальные состояния применяем)
def Get_uniq_lin_eq(lin_eqs, L, k, k_prev, a_prev):

    # массив для хранения уникальных линейных соотношений
    uniq_lin_eqs = []
    # массив для суммирования в него результатов гаммы
    uniq_gamma_eqs = []

    mask = (2**k-1) << (L-(k+k_prev))
    for (lin_eq, gamma_eq) in lin_eqs:
        sum_prev_bit = sum(int(i) for i in bin((lin_eq >> (L-k_prev)) & a_prev)[2:])%2
        significant_lin_eq = (lin_eq & mask) >> (L-(k+k_prev))
        
        # так как теперь у нас не бит в правой части равенства,
        # а разница между соотношениями с нулем в правой части и с единицей,
        # то мы пытаемся выяснить знак (а для него и бит), который получится
        # после суммирования значения sum_prev_bit и "победившего" значения gamma_eq (его знак)
        gamma_eq = abs(gamma_eq) * (-1 if np.sign(gamma_eq) != (-1)**sum_prev_bit else 1)
        
        index = bisect_left(uniq_lin_eqs, significant_lin_eq)
        if index == len(uniq_lin_eqs) or uniq_lin_eqs[index] != significant_lin_eq:
            uniq_lin_eqs.insert(index, significant_lin_eq)
            uniq_gamma_eqs.insert(index, gamma_eq)
        elif uniq_lin_eqs[index] == significant_lin_eq:
            uniq_gamma_eqs[index] += gamma_eq

    return Normalize_gamma(uniq_lin_eqs, uniq_gamma_eqs)


# рассчитываем значение вспомогательной функции h
def Get_value_h(lin_eqs, k):
    q = 2**k
    h = [ 0 for _ in range(q) ]
    h[0] = 1 # потому что -1^{0}=1
    for lin_eq, gamma_eq in lin_eqs:
        h[lin_eq] = gamma_eq
    return h

# преобразование Уолша-Адамара 1-го рода
def fastWalsh(val_h):
    # руководствуемся идеями, описанными в статье
    l = len(val_h)//2

    if (l != 0):
        value_H_1 = fastWalsh( [ val_h[i]+val_h[l+i] for i in range(l) ] )
        value_H_2 = fastWalsh( [ val_h[i]-val_h[l+i] for i in range(l) ] ) 
        return value_H_1+value_H_2
    
    return val_h

def Get_omega(uniq_lin_eqs):
    return len(uniq_lin_eqs)


def Get_T(omega, t, eps):
    return omega*2**(t-2)*eps**(t)

def Calc_m(omega, t, eps):
    return sqrt(omega)*2**(t)*eps**(t)

# один шаг атаки
def Pass(k, k_prev, t, L, a_prev, lin_eqs, eps):    
    # прежде чем заполнять массив h,
    # нам необходимо найти наиболее вероятные результаты для линейных соотношений
    uniq_lin_eqs = Get_uniq_lin_eq(lin_eqs, L, k, k_prev, a_prev)

    omega = Get_omega(uniq_lin_eqs)
    print(f"omega: {omega}")

    m = Calc_m(omega, t, eps)
    # расстояние между центрами распределений должно быть больше 3х сигм, 
    # чтобы мы могли хорого различать гипотезы
    if m < 3:
        print(f"m: {m}")

    T = Get_T(omega, t, eps)

    value_h = Get_value_h(uniq_lin_eqs, k)

    value_H = fastWalsh(value_h)

    max_value_H = max(value_H)

    # отладочные принты, для наглядности атаки
    print(f"a_prev: {bin(a_prev)}")
    print(f"T: {T}")
    print(f"max in H: {max_value_H}")
    #inp = input()

    # все подошедшие состояния
    a = []
    # если нет значений, больше граничного,
    # то нечего и стараться
    if max_value_H < T:
        return a

    for i, h in enumerate(value_H):
        if (h > T):
            a.append((a_prev<<k)^i)

    # возвращаем все подошедшие состояния
    return a


# обработка одного регистра сдвига
def oneLFSR(p, k_i, poly, z, count_of_parts):
    
    print("начинаем работу с новым регистром сдвига:")
    G = Gen_G(poly)

    L = len(G)
    # получаем "утекающую вероятность"
    if (p > 0.5):
        eps = p - 0.5
    else:
        eps = 0.5 - p
        #инвертируем элементы GF2 из массива z
        z = [i^1 for i in z]

    # массив уже подобранных бит РСЛОС
    # изначально нет подобранных бит
    a_prev = [ 0 ]

    # переменная, содержащая длину предыдущих подобраных бит РСЛОС
    k_prev = 0

    # восстанавливаем РСЛОС по частям:
    for k in k_i:
        lin_eqs, t = Gen_lin_eq(G, k, k_prev, z, count_of_parts)

        # массив, в который будут складываться состояния, подобранные на этом шаге
        a = []
        # проверяем каждое возможное значение кусочка РСЛОС
        for a_i in a_prev:
            a += Pass(k, k_prev, t, L, a_i, lin_eqs, eps)

        # обновляем массив начальных состояний для следующего шага цикла 
        # (только уникальные элементы)
        a_prev = []
        for a_i in a:
            if a_i not in a_prev:
                a_prev.append(a_i)

        k_prev += k

        # если мы хотим дебажить по шагам
        #print(f"a = \n{[bin(a_i)[2:] for a_i in a]}")
        print(f"len_a: {len(a)}")
        #inp = input()

        if( len(a_prev) == 0 ):
            return []

    return a_prev


def Load_gamma(filename):
    filename = f"{filename}.json"
    f = open(filename, 'r')
    dict = json.load(f)
    return dict["g"]


def main():
    filename = "output"
    z = Load_gamma(filename)
    p = Get_p(0)

    print("рассчитаем все корреляционные вероятности")
    for i in range(len(pickup_points)):
        print(f"p[{i}]: {Get_p(i)}")


    k_i = [24,24]
    # количество отрезков, на которые мы разделим те биты,
    # которые хотим обнулить при составлении линейных уравнений проверки четности
    count_of_parts = 2
    a = oneLFSR(p, k_i, fpoly, z, count_of_parts)
    print("-------------------------")
    print([bin(answ) for answ in a])
    if len(a) == 0:
        print("не найдено ни одного начального состояния")
        return

    st = [int(i) for i in bin(a[0])[2:]]
    # при использовании в LFSR начальное заполнение переворачивается -
    # учтем данную особенность
    st.reverse()
    # прокручиваем регистр назад по одному шагу за раз
    for _ in range(7):
        # сделаем крайний бит нулем
        st_new = st[1:]+[0]
        L = LFSR(fpoly=fpoly,initstate = st_new)
        L.runKCycle(1)
        # крайний бит всегда участвует в формировании нового бита состояния,
        # поэтому если состяние не изменилось, то он ноль, иначе - единица
        st_new[-1] = L.state[0]^st[0]
        st = st_new[::]
    
    # ура, мы имеем секретный init_state, получаем из него флаг
    print("0b"+"".join([str(s) for s in st]))
    bt = long_to_bytes(int("".join([str(i) for i in st]),2))
    flag = b64encode(bt).decode()
    print("CUP{"+flag+"}")


if __name__ == '__main__':
    main()