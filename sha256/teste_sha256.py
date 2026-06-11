from sha256 import sha256
import hashlib
msg = b'abc'
print(sha256(msg))           
print(hashlib.sha256(msg).hexdigest())  
