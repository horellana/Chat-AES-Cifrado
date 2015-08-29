import sys

from Crypto.Cipher import AES
from Crypto import Random


class Enigma: ### juejuejue
    def __init__(self, key):
        self.key = key
    
    def cifrar(self, mensaje):
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return iv + cipher.encrypt(mensaje)

    def decifrar(self, mensaje):
        iv = mensaje[0:len(self.key)]
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return cipher.decrypt(mensaje)[len(self.key):]

if __name__ == '__main__':
    key = 'jhgthebnshdkfjeh'
    e = Enigma(key)
    cifrado = e.cifrar(sys.argv[1])

    print('Cifrado: {}'.format(cifrado))
    print('Sin cifrar: {}'.format(e.decifrar(cifrado)))
