from hashlib import sha256

from cryptography.fernet import Fernet


def generate_key(password):
    return sha256(password.encode()).digest()


def encrypt(plaintext, key):
    f = Fernet(key)
    return f.encrypt(plaintext.encode()).decode()


def decrypt(ciphertext, key):
    f = Fernet(key)
    return f.decrypt(ciphertext).decode()
