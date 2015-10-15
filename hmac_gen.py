import hashlib
import hmac

class hmacGenerator:


    def __init__(self, key, msg):
        self.key = key
        self.msg = msg


    def genHmac(self):
        result = hmac.new(self.key, self.msg, hashlib.md5).hexdigest()
        return result		