import unittest
import cbc
# from cbc import CBC


class EncryptionTest(unittest.TestCase):

	message = "this is a message"
	def setUp(self):
		iv = cbc.generateIV()
		key = cbc.generateKey()
		self.encryptCipher = cbc.generateCBC(key,iv)
		self.decryptCipher = cbc.generateCBC(key,iv)


	def test(self):
		cipherText = cbc.encrypt(self.encryptCipher, self.message)
		print cipherText
		plainText = cbc.decrypt(self.decryptCipher, cipherText)
		print plainText
		self.assertEqual(plainText, self.message)


if __name__ == '__main__':
    unittest.main()