#! /usr/bin/env python3

import json
from Crypto.Util.number import long_to_bytes


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


def MontMul(x, y, n):
    xy, time, extra = MontMulTime(x, y, n, r, n_inverse, 0)
    return xy, extra


def updateMessages(messages, currentKey, n):
    currentSet = messages[:]
    for i in range(len(messages)):
        currentSet[i] = MontMul(currentSet[i], currentSet[i], n)[0]

    for i in range(len(messages)):
        for j in range(1, len(currentKey)):
            if(currentKey[j] == "1"):
                currentSet[i] = MontMul(currentSet[i], messages[i], n)[0]
            currentSet[i] = MontMul(currentSet[i], currentSet[i], n)[0]
    return currentSet


def checkKey( messages, times, d, n):
    if all(MontExp(m, n, d+"1")[1] == t for m,t in zip(messages, times)):
        return (1, "1")
    if all(MontExp(m, n, d+"0")[1] == t for m,t in zip(messages, times)):
        return (1, "0")
    return (0, "0")


def checkAnormal(diff1, diff2):
    print("diff1: ", diff1, " diff2: ", diff2)
    print("diff1-diff2", abs(diff1 - diff2))
    if (abs(diff1 - diff2) < treshold) | ((diff1 < 0) & (diff2 < 0)):
        print("Anormal!!!")
        return 1
    return 0


class Group(object):
    time = 0
    size = 0


def simulateStep( mont_messages, currentSet, n, groups, time  ):
    encoded_1 = currentSet[:]
    encoded_0 = currentSet[:]
    for i in range(len(mont_messages)):
        # предположим, что бит j равен 0
        (encoded_0[i], extra) = MontMul(currentSet[i], currentSet[i], n)
        # если произошла дополнительная редукция
        if extra :
            groups[3].time += time[i]
            groups[3].size += 1
        # если не произошло дополнительной редукции
        else :
            groups[4].time += time[i]
            groups[4].size += 1

        # предположим, что бит j равен 1
        (temp, extra) = MontMul(currentSet[i], mont_messages[i], n)
        (encoded_1[i], extra) = MontMul(temp, temp, n)

        # если произошла дополнительная редукция
        if extra :
            groups[1].time += time[i]
            groups[1].size +=1
        # если не произошло дополнительной редукции
        else :
            groups[2].time += time[i]
            groups[2].size +=1
    return (groups, encoded_0, encoded_1)


def compute_differences( groups ):

    print("groups size: ", groups[1].size, groups[2].size, groups[3].size, groups[4].size)

    # вычисляем среднее время для всех 4 групп
    uF1 = float(groups[1].time)/groups[1].size
    uF2 = float(groups[2].time)/groups[2].size
    uF3 = float(groups[3].time)/groups[3].size
    uF4 = float(groups[4].time)/groups[4].size

    # вычисляем разницу между парныыми группами
    diff1 = uF1 - uF2
    diff2 = uF3 - uF4

    return (diff1, diff2)


def look_Ahead(bitCheck, encoded_0, encoded_1, messages, mont_messages, n, time, key):
    global lookAhead

    delta = 0
    key += str(bitCheck)
    validKey, bit = checkKey(messages, time, key, n)
    if validKey :
        key += str(bit)
        return (validKey, key, delta)

    if bitCheck :
        temp_encoded  = encoded_1[:]
    else:
        temp_encoded  = encoded_0[:]

    for y in range(lookAhead):
        groups  = [ Group() for i in range(5)]
        (groups, encoded_0, encoded_1 ) = simulateStep( mont_messages, temp_encoded, n, groups, time );
        (diff1, diff2) = compute_differences( groups )

        bit = 0
        if diff1 > diff2:
            bit = 1

        if bit :
            temp_encoded = encoded_1[:]
        else:
            temp_encoded = encoded_0[:]
        key += str(bit)
        validKey, bit = checkKey(messages, time, key, n)
        if validKey :
            key += str(bit)
            return (validKey, key, delta)

        if not checkAnormal(diff1, diff2) :
            delta += abs(int(diff1 - diff2))

    return (validKey, key, delta)


def Load_messages_and_time(filename):
    filename = f"{filename}.json"
    f = open(filename, 'r')
    dict = json.load(f)
    return dict["m"], dict["t"]


def attack(n, filename):
    global sampleSize

    validKey = 0
    keySize  = 21*8
    foundKey = "1"

    # пока ключ находится в пределах максимального ключа и он неверен
    while (keySize < maxKeySize) &  (not validKey):

        # все реинициализируем
        mont_messages   = []
        currentSet      = []
        stablekeySet    = 0
        error           = 0

        # загружаем сообщения из полученного в задании файлика
        messages, time = Load_messages_and_time(filename)

        # сбрасываем ключ до стабильного ключа
        currentKey = foundKey

        for i in range(len(messages)):
            # преобразовываем каждое сообщение в форму Монтгомери
            mont_messages.append(MontMul(messages[i], r_square, n)[0])

        print("Sample Size: ", sampleSize)
        print("Start from key bit ", len(currentKey))


        currentSet = updateMessages(mont_messages, currentKey, n)
        encoded_1 = currentSet[:]
        encoded_0 = currentSet[:]

        # обнаруживаем следующие биты до последнего бита, который мы угадаем
        while ((len( currentKey ) <= keySize) & (error < 7)):
            warning = 0
            groups  = [ Group() for i in range(5)]

            (groups, encoded_0, encoded_1 ) = simulateStep( mont_messages, currentSet, n, groups, time )

            (diff1, diff2) = compute_differences( groups )

            # условие нормального поведения
            if checkAnormal(diff1, diff2) :
                warning = 1
                error += 2
            else :
                if error > 0:
                    error -= 1
                warning = 0

            if warning > 0 :
                print("warning at bit", len(currentKey))
                stablekeySet = 1

                # проверяем предыдущие раунды для бита 1
                (validKey, possibleKey, delta0) = look_Ahead(0, encoded_0, encoded_1, messages, mont_messages, n, time, currentKey)
                if(validKey):
                    return possibleKey

                # проверяем предыдущие раунды для бита 1
                (validKey, possibleKey, delta1) = look_Ahead(1, encoded_0, encoded_1, messages, mont_messages, n, time, currentKey)
                if(validKey):
                    return possibleKey

                # решаем, какой набор был лучше
                if(delta0 < delta1) :
                    bit = 1
                else :
                    bit = 0

            else :
                # если разница для групп с предполагаемым битом = 1 больше, 
                # чем разница групп с предполагаемым битом = 0, то предсказать 1, 
                # иначе предсказать 0
                if diff1 > diff2:
                    bit = 1
                else :
                    bit = 0

                if(not stablekeySet):
                    foundKey = currentKey

            # в зависимости от того, какой бит предсказан, 
            # сохранить результаты, вычисленные с этим битом, для следующего раунда
            if bit == 1:
                currentSet = encoded_1[:]
            else:
                currentSet = encoded_0[:]

            # добавляем предсказанный бит к ключу
            currentKey += str(bit)
            print("currentKey: ", currentKey)
            validKey, bit = checkKey(messages, time, currentKey, n)
            if validKey:
                return currentKey + str(bit)


        print(f"try again")
        print(f"input something")
        inp = input()
        keySize += 16
        sampleSize += 1000

    return currentKey


def main():
    n = 0xae3e389e58e03bcf77603520dfb1f6bb5ff1f36edddb24caf0fb34e16a656a8d2235fd27bda069374d0a96c5463c53af42edd0c0d3dea019bced0b90007ff6262642a233974b0d31158ab210d831c5fb9dc42f393960a26c71c2b9c489848ddfca191f054d57b30f7201cd3d3fe7ad1b80817abe41299df61224c0c93c8717f9

    global sampleSize
    sampleSize = 12000
    global maxKeySize
    maxKeySize = 256
    global treshold
    treshold = 15
    global lookAhead
    lookAhead = 3

    filename = "output"

    # переменные, необходимые для умножения Монтгомери
    # эти константы могут быть вычислены один раз для всех дальнейших возведений в степень
    global r
    r = (int)(pow(2, len(bin(n)[2:])))
    global n_inverse
    n_inverse = (int)(pow(-n,-1,r))
    global r_square
    r_square = (int)(pow(r,2,n))

    # Execute a function representing the attacker.
    key = int(attack(n, filename),2)

    print("FOUND KEY = ", hex(key))

    enc_flag = 0x92c831bb93f59bedaaa46b656bc4208065ddcace7c
    flag = long_to_bytes(enc_flag^key)
    print(b'CUP{'+flag+b'}')
    

if __name__ == "__main__":
    main()