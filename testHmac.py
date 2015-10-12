import unittest
from hmac_gen import hmacGenerator

class hmacTest(unittest.TestCase):

	def setUp(self):
		key = "TESTKEY"
		message = "THISTHETESTMESSAGE"
		self.alpha = hmacGenerator(key, message);
		self.beta = hmacGenerator(key, message);

	def test(self):
		ahex = self.alpha.genHmac()
		bhex = self.beta.genHmac()

		print ahex
		print bhex
		
		self.assertEqual(ahex,bhex)

	