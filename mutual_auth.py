import random
from Crypto.Cipher import AES
import md5
import time

class MutualAuth:

    def __init__(self, shared_secret, name):
        self.shared_secret = shared_secret
        self.IV = 'IVIVIVIVIVIVIVIV'
        self.aes = AES.new(self.shared_secret, AES.MODE_CFB, self.IV)
        self.name = name

    def generate_nonce(self, bits):
        nonce = random.getrandbits(bits) # bits needs to be at least 1000
        self.nonce = str(nonce)
        return nonce

    def encrypt_nonce(self, nonce_received, dh_value):
        print "-------" + self.name + " is encrypting at time " + str(time.time())
        return self.aes.encrypt(str(self.name)+','+str(nonce_received)+','+str(dh_value))

    def decrypt_ciphertext(self, ciphertext):
        print "-------" + self.name + "is decrypting at time " + str(time.time())
        return self.aes.decrypt(ciphertext)

    def check_name(self, plaintext):   
        return self.name in plaintext

    def check_nonce(self, plaintext):  
        return str(self.nonce) in plaintext

    def get_partner_dh_value(self, plaintext):
        dh_value = plaintext.split(',')[2]
        return int(dh_value)