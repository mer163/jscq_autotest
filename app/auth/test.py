import hashlib


if __name__ == '__main__':
    m = hashlib.md5()
    m.update('123456'.encode())
    psw = m.hexdigest()
    print(psw)
    print(range(3,5)[1])