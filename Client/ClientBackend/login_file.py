import os
import json

from Client.ClientBackend.config import BASE_DIR, WRITE_MOD, JSON_INDENT, FILE_BEGIN
from Client.ClientBackend.utils import key_from_base64, key_to_base64


class LoginFile:
    LOGIN_FILENAME = "login_file.json"
    LOGIN_USERNAME = "user"
    LOGIN_PASSWORD = "password"

    def __init__(self):
        if not self._is_file_exists():
            with open(os.path.join(BASE_DIR, LoginFile.LOGIN_FILENAME), WRITE_MOD) as login_json:
                json.dump((), login_json, indent=JSON_INDENT)

    def _is_file_exists(self):
        return os.path.isfile(os.path.join(BASE_DIR, LoginFile.LOGIN_FILENAME))

    def save(self, user_name, encrypted_password):
        with open(os.path.join(BASE_DIR, LoginFile.LOGIN_FILENAME), WRITE_MOD) as login_json:
            login_data = json.load(login_json)
            login_data.update({LoginFile.LOGIN_USERNAME: user_name,
                               LoginFile.LOGIN_PASSWORD: encrypted_password})
            json.dump(login_data, login_json, indent=JSON_INDENT)

    def load(self, user_name):
        with open(os.path.join(BASE_DIR, LoginFile.LOGIN_FILENAME), WRITE_MOD) as login_json:
            login_data = json.load(login_json)
            for user_details in login_data:
                if user_details[LoginFile.LOGIN_USERNAME] == user_name:
                    return user_details[LoginFile.LOGIN_PASSWORD]
        # TODO raise exception

    def verify(self, user_name):
        with open(os.path.join(BASE_DIR, LoginFile.LOGIN_FILENAME), WRITE_MOD) as login_json:
            login_data = json.load(login_json)
            if user_name in login_data:
                return True
            return False
