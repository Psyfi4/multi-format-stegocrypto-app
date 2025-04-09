
from Crypto.Cipher import AES
import base64

def pad(text):
    return text + (16 - len(text) % 16) * chr(16 - len(text) % 16)

def unpad(text):
    return text[:-ord(text[-1])]

def encrypt_message(message, key):
    key = key.encode('utf-8')
    cipher = AES.new(key, AES.MODE_ECB)
    padded = pad(message)
    encrypted = cipher.encrypt(padded.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_message(encrypted, key):
    key = key.encode('utf-8')
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(encrypted))
    return unpad(decrypted.decode('utf-8'))
