#! /usr/bin/env python3

from string import printable


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


def Restore_from_crc(pre_text, after_text, crc, poly):
    table_forward = Gen_table(poly)
    # Build reverse table
    table_reverse = [0] * 256

    for i in range(256):
        table_reverse[CRC(chr(i), poly) & 0xff] = CRC(chr(i), poly)

    # restore crc val from after_text
    reg_val = crc
    for a in after_text[::-1]:
        high_bits = reg_val & 0xff
        reg_val ^= table_reverse[high_bits]
        reg_val >>= 8
        reg_val |= (table_forward.index(Divide_val_by_bytes(table_reverse[high_bits],16))^ord(a))<<120

    # Reverse CRC
    rev_crc = []
    for i in range(16):
        high_bits = reg_val & 0xff
        reg_val ^= table_reverse[high_bits] # xor with left operand
        reg_val >>= 8 # adjust right operand
        rev_crc.append(high_bits)

    # Build CRC
    result = ''
    header_crc = CRC(pre_text, poly)
    cur_high_bits = header_crc >> 120

    for rev_byte in rev_crc[::-1]:
        recovered = table_forward.index(Divide_val_by_bytes(table_reverse[rev_byte],16)) ^ cur_high_bits
        cur_high_bits = CRC(pre_text+result + chr(recovered), poly) >> 120
        result += chr(recovered)

    return result


def main():
    poly = 0x1fd731378020ec665bcf15be944e08f0b
    pre_text = "A very important task!!! Gotta drop the flag CUP{"
    after_text = "}!!!"
    crc = int(open("output.txt", "r").readline())
    flag = Restore_from_crc(pre_text, after_text, crc, poly)
    print("CUP{"+flag+"}")


if __name__ == '__main__':
    main()