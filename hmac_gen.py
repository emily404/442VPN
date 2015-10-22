import hashlib
import hmac

def genHmac(key, msg):
	return hmac.new(key, msg, hashlib.md5).hexdigest()
