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
        iv = mensaje[0:16]
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return cipher.decrypt(mensaje)[16:]
