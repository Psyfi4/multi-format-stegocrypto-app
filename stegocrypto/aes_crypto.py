from Crypto.Cipher import AES
import base64

def pad(s): return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
def unpad(s): return s[:-ord(s[-1])]

def encrypt_message(message, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    ct_bytes = cipher.encrypt(pad(message).encode())
    return base64.b64encode(ct_bytes).decode()

def decrypt_message(ciphertext, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    pt = cipher.decrypt(base64.b64decode(ciphertext)).decode()
    return unpad(pt)
