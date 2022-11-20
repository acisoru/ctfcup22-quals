#! /usr/bin/env python3

def main():
    f_in = open("picture.jpeg", "rb")
    f_out = open("picture.jpeg.encrypted", "wb")
    key = 252
    for b in f_in.read():
        f_out.write(bytes([b^key]))
        key = b
    f_in.close()
    f_out.close()


if __name__ == '__main__':
    main()