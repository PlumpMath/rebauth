'''
RebAuth : Rebirth Authentication
Webkit webbrowser that manages your authentication/personal information automatically, periodically.
'''
from Crypto.Cipher import AES
from Crypto.Random import random
from Crypto.Hash import SHA256
from Crypto.Util import Counter

import clientMain, serverMain

hash=lambda msg : SHA256.new(msg.encode()).digest()
__all__=['Cryptor', 'clientMain', 'serverMain', 'hash']

class Cryptor():
    hash = hash
    def __init__(self,key,counter):
        self._encryptor = AES.new(key,AES.MODE_CTR,counter=Counter.new(128,initial_value=counter))
    def encrypt(self,msg):
        return self._encryptor.encrypt(msg)
    def decrypt(self,code):
        return self._encryptor.decrypt(code).decode(errors='ignore')

random = random.getrandbits
# def random(bit):
#   return random.getrandbits(bit)