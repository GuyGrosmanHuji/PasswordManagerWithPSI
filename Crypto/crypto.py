import base64

from cryptography.fernet import Fernet

# TODO we should have a unique SALT key for generating key. Currently it is a constant but it is
#  unsafe, how should we save it and load it?
SALT = b'2c\x10\xab\x10\xa5\x1e\x0ba\xfb%\xba\xa0\xcd\xdb\x9a'
KEY_LENGTH = 32
KEY_GENERATION_ITERATIONS = 390000

def generate_key(password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=SALT,
        iterations=KEY_GENERATION_ITERATIONS,
    )
    return kdf.derive(password.encode())


def verify_key(password, key):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=SALT,
        iterations=KEY,
    )
    return kdf.verify(password.encode(), key)


def to_base64(att):
    return base64.urlsafe_b64encode(att)


def from_base64(att):
    return base64.urlsafe_b64decode(att)


def encrypt(plaintext, key):
    f = Fernet(key)
    return f.encrypt(plaintext.encode(), key)

def decrypt(ciphertext, key):
    f = Fernet(key)
    return f.decrypt(ciphertext).decode()
