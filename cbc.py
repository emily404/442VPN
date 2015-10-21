from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE = 16

def generateIV():
	initializationVector = Random.new().read(BLOCK_SIZE)
	return initializationVector

def generateKey():
	key = Random.new().read(BLOCK_SIZE)
	return key

pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

def generateCBC(key, iv):
	return AES.new(key, AES.MODE_CBC, iv)

def encrypt(cipher, plainText):
	cipherText = cipher.encrypt(pad(plainText))
	return cipherText

def decrypt(cipher, cipherText):
	plainText = unpad(cipher.decrypt(cipherText))
	return plainText



