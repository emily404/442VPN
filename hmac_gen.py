import hashlib
import hmac


def genHmac(key, msg):
	return hmac.new(key, msg, haslib.md5).hexdigest()

	