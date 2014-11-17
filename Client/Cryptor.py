from Singleton import Singleton
from Crypto import Cipher
from Crypto.Cipher import AES
from Crypto.Random import random
from Crypto.Hash import SHA256
from Crypto.Util import Counter

class Cryptor():
  hash=lambda msg : SHA256.new(msg).digest()
  def __init__(self,key,counter):
    self.encryptor = AES.new(key,AES.MODE_CTR,counter=Counter.new(128,initial_value=counter))
  # def hash(self,msg):
  #   return SHA256.new(msg).digest()
  def encrypt(self,msg):
    return self.encryptor.encrypt(msg)