#! /usr/bin/env python3


def Divide_val_by_bytes(val, len_reg):
    return [ (val&(0xff<<(8*(pos))))>>(8*(pos)) for pos in range(len_reg-1,-1,-1)]


def From_byte_mas_to_val(byte_mas):
    return sum(r<<(8*(len(byte_mas)-i-1)) for i,r in enumerate(byte_mas))


def Gen_table(poly):
    # deg of poly 
    W = len(bin(poly)[2:])-1
    crc_table=[]
    for byte in range(256):
        operator= byte<<(W-8)
        mask = 1<<(W-1)
        for bit in range(8):
            if (operator & mask) != 0:
                operator <<= 1
                operator ^= poly
            else:
                operator <<= 1
        crc_table.append(Divide_val_by_bytes(operator, W//8))
    return crc_table


def CRC(text, poly):
    text = [ord(t) for t in text]
    # deg of poly 
    W = len(bin(poly)[2:])-1
    len_reg = W//8
    T = Gen_table(poly)

    reg = [0 for _ in range(len_reg)]
    for a in text:
        idx = a^reg.pop(0)
        reg.append(0)
        reg = [r^t for r,t in zip(reg,T[idx])]

    return From_byte_mas_to_val(reg)


def main():
    poly = 0x1fd731378020ec665bcf15be944e08f0b
    pre_text = "A very important task!!! Gotta drop the flag CUP{"
    flag = "****************"
    after_text = "}!!!"
    print(CRC(pre_text+flag+after_text, poly))


if __name__ == '__main__':
    main()