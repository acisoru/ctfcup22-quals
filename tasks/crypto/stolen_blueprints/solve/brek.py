#! /usr/bin/env python3

def main():
    f_in = open("picture.jpeg.encrypted", "rb")
    f_out = open("picture.jpeg", "wb")
    key = 252
    for b in f_in.read():
        key = b^key
        f_out.write(bytes([key]))
    f_in.close()
    f_out.close()


if __name__ == '__main__':
    main()