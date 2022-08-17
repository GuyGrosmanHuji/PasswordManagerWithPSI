import os

from Client.ClientBackend.login_file import LoginFile
from Client.ClientBackend.passwords_file import PasswordsFile

from Crypto.crypto import *


class Backend:
    def __init__(self):
        self.login_file = LoginFile()
        self.passwords_file = PasswordsFile()

    def save_user(self, user_name, password):
        if self._verify_user(user_name):
            # TODO this user already signed-up
            raise Exception
        user_key = generate_key(password)
        encrypted_password = encrypt(password, user_key)
        # we want to the encrypted password as a string
        encrypted_password = encrypted_password.decode()
        self.login_file.save(user_name, encrypted_password)

    def load_user(self, user_name, password):
        if not self._verify_user(user_name):
            # TODO there is no such user
            raise Exception
        encrypted_password = self.login_file.load(user_name)
        # we render the encrypted password to bytes
        encrypted_password = encrypted_password.encode()
        key = generate_key(password)
        decrypted_password = decrypt(encrypted_password, key)
        if password != decrypted_password:
            # TODO wrong password exception
            raise Exception
        # key = user_key
        return key


    def _verify_user(self, user_name):
        return self.login_file.verify(user_name)


