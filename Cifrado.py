from Crypto.Cipher import AES
from Crypto import Random


class Enigma: ### juejuejue
    def __init__(self, key):
        self.key = key
    
    def cifrar(self, mensaje):
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return cipher.encrypt(mensaje)

    def decifrar(self, mensaje):
        iv = mensaje.read(16)
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return cipher.decrypt(mensaje, self.key)[len(self.key):]
