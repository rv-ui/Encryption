from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Generate key for encyption and decryption
#basic key
#simple_key = get_random_bytes(32)
#print(simple_key)
static_salt = b"r@y2M\xfc\xf6\xe6\n\x82\xb9\xce0Y)\x17Nd\xe3_\xc2\xfd^\n&sRdx'\xb8\xfc"
password = "brdbrn@93"

#actaual encryption key generation
key = PBKDF2(password, static_salt, dkLen=32)
#print(key)

with open('encrypt.bin', 'rb') as f:
    iv=f.read(16)
    decrypt_data = f.read()
    
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
original_data = unpad(cipher.decrypt(decrypt_data), AES.block_size)
print(original_data)
