import unittest
from mutual_auth import MutualAuth

class MutualAuthTest(unittest.TestCase):

	def setUp(self):
		shared_secret = 'secretsecretsecretsecret'
		name_alice = 'alice'
		name_bob = 'bob'
		self.alice = MutualAuth(shared_secret, name_alice)
		self.bob = MutualAuth(shared_secret, name_bob)
		self.alice_dh = 17
		self.bob_dh = 3

	def test(self):
		bits = 100
		# alice send ra
		ra = self.alice.generate_nonce(bits)
		
		# bob use ra to encrypt eb and send rb
		eb = self.bob.encrypt_nonce(ra, self.bob_dh)
		rb = self.bob.generate_nonce(bits)

		# alice validate eb encrypted by bob
		plaintext = self.alice.decrypt_ciphertext(eb)
		# alice's own name not in plaintext
		self.assertFalse(self.alice.check_name(plaintext))
		# alice's nonce is in plaintext
		self.assertTrue(self.alice.check_nonce(plaintext))
		# get bob's dh
		self.assertEquals(str(self.bob_dh), self.alice.get_partner_dh_value(plaintext))

		# alice use rb to encrypt ea encryted by alice
		ea = self.alice.encrypt_nonce(rb, self.alice_dh)

		# bob validates ea
		plaintext = self.bob.decrypt_ciphertext(ea)
		# bob's own name not in plaintext
		self.assertFalse(self.bob.check_name(plaintext))
		# bob's nonce is in plaintext
		self.assertTrue(self.bob.check_nonce(plaintext))
		# get alice's dh
		self.assertEquals(str(self.alice_dh), self.bob.get_partner_dh_value(plaintext))
		
if __name__ == '__main__':
    unittest.main()