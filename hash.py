import hashlib
BLOCKSIZE = 65536
hasher = hashlib.sha3_512()
with open('Prueba.txt', 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(BLOCKSIZE)
print(hasher.hexdigest())

input('FINALIZADO')