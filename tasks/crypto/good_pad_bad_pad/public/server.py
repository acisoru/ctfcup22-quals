from Crypto.Util.number import bytes_to_long

random1 = 30*b'*'
message = 32*b'*'
m0 = message+random1

# msg должно иметь длину 62 байта
def PKCS(id,msg,e,N):
    m = bytes_to_long(id+msg)
    return pow(m,e,N)