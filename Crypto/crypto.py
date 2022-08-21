import sys
from hashlib import sha256
import base64

from cryptography.fernet import Fernet


def hash_password(password: str) -> int:
    return int.from_bytes(sha256(password.encode()).digest()[0:4], byteorder=sys.byteorder)


def generate_key(password: str) -> bytes:
    return base64.urlsafe_b64encode(sha256(password.encode()).digest())


def encrypt(plaintext: str, key: bytes) -> str:
    f = Fernet(key)
    return f.encrypt(plaintext.encode()).decode()


def decrypt(ciphertext: str, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(ciphertext.encode()).decode()
