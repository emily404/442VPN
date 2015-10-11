import unittest
from diffie_hellman import DiffieHellman

class DiffieHellmanTest(unittest.TestCase):

	def setUp(self):
		# sharedSecret = 17
		base = 5
		modulo = 23
		self.alice = DiffieHellman(modulo, base)
		self.bob = DiffieHellman(modulo, base)

	def test(self):
		aPair = self.alice.sessionKeyGen()
		bPair = self.bob.sessionKeyGen()

		a = self.alice.sessionKeyDecrypt(bPair[0])
		b = self.bob.sessionKeyDecrypt(aPair[0])

		self.assertEqual(a,b)


if __name__ == '__main__':
    unittest.main()