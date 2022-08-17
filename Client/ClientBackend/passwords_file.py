import os
import json

from Client.ClientBackend.config import BASE_DIR, WRITE_MOD, JSON_INDENT, FILE_BEGIN


class PasswordsFile:
    PASSWORDS_FILENAME = "passwords.json"
    USERNAME = "user"
    # TODO Currently we only support login name and login password. No domain associated with
    #  these i.e., we don't relate there login details to website or a service
    LOGIN_NAME = "login_name"
    LOGIN_PASSWORD = "login_password"

    def __init__(self):
        if not self._is_file_exists():
            with open(os.path.join(BASE_DIR, PasswordsFile.LOGIN_FILENAME), WRITE_MOD) as \
                    passwords_json:
                json.dump((), passwords_json, indent=JSON_INDENT)

    def _is_file_exists(self):
        return os.path.isfile(os.path.join(BASE_DIR, PasswordsFile.LOGIN_FILENAME))

    def add_login_details(self, user_name, encrypted_login_username, encrypted_login_password):
        with open(os.path.join(BASE_DIR, PasswordsFile.PASSWORDS_FILENAME), WRITE_MOD) as pws_json:
            pws_data = json.load(pw_json)
            if user_name not in pws_data:
                pws_data[user_name] = {}
            pws_data[user_name].update({PasswordsFile.LOGIN_USERNAME: encrypted_login_username,
                                        PasswordsFile.LOGIN_PASSWORD: encrypted_login_password})
            json.dump(pws_data, pw_json, indent=JSON_INDENT)

    def get_user_passwords(self, user_name):
        with open(os.path.join(BASE_DIR, PasswordsFile.PASSWORDS_FILENAME),
                  WRITE_MOD) as login_json:
            login_data = json.load(login_json)
            return login_data[user_name].values()

    def get_password(self, user_name, encrypted_login_username):
        with open(os.path.join(BASE_DIR, PasswordsFile.PASSWORDS_FILENAME),
                  WRITE_MOD) as login_json:
            login_data = json.load(login_json)
            return login_data[user_name][encrypted_login_username]

    def get_user_login_names(self, user_name):
        with open(os.path.join(BASE_DIR, PasswordsFile.PASSWORDS_FILENAME),
                  WRITE_MOD) as login_json:
            login_data = json.load(login_json)
            return login_data[user_name].keys()
