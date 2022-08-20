import os
import json
import random
import string

from typing import Union, Dict, List, Tuple

from Client.ClientBackend.exceptions import *
from Client.ClientBackend.config import *

from Crypto.crypto import generate_key, encrypt, decrypt


class UsersTable:
    USERS_TABLE_FILENAME = "users_table.json"
    USERNAME = "username"
    PASSWORDS = "passwords"
    LOGIN_SITE = "login_site"
    LOGIN_USERNAME = "login_username"
    LOGIN_PASSWORD = "login_password"

    DUMMY_LENGTH = 16

    USERNAME_IDX = 0
    PASSWORD_IDX = 1

    def __init__(self, username: str, password: str, mode=SIGN_UP_MODE):
        if not os.path.isfile(os.path.join(BASE_DIR, UsersTable.USERS_TABLE_FILENAME)):
            with open(os.path.join(BASE_DIR, UsersTable.USERS_TABLE_FILENAME),
                      WRITE_MODE) as login_json:
                json.dump((), login_json, indent=JSON_INDENT)
        self.username = username
        self.master_key = generate_key(password)
        if mode == SIGN_UP_MODE:
            self.register()
        elif mode == SIGN_IN_MODE:
            self.verify()

    def register(self):
        with open(os.path.join(BASE_DIR, UsersTable.USERS_TABLE_FILENAME), WRITE_MODE) as table:
            table_data = json.load(table)
            if self.username in table_data.keys():
                raise UnavailableUsername("This username is unavailable.")
            login_details = self._generate_dummy_login_details()
            encrypted_login_details = self._encrypt_login_details(login_details)
            encrypted_login_details = UsersTable._arrange_login_details(encrypted_login_details)
            table_data[self.username] = {}
            passwords = table_data[self.username].update(encrypted_login_details)
            table_data.update({UsersTable.USERNAME: self.username, UsersTable.PASSWORDS: passwords})
            json.dump(table_data, table, indent=JSON_INDENT)

    def save(self, login_details: Union[List[str], Tuple[str]]):
        with open(os.path.join(BASE_DIR, UsersTable.USERS_TABLE_FILENAME), WRITE_MODE) as table:
            table_data = json.load(table)
            encrypted_login_details = self._encrypt_login_details(login_details)
            encrypted_login_details = UsersTable._arrange_login_details(encrypted_login_details)
            passwords = table_data[self.username].update(encrypted_login_details)
            table_data.update({UsersTable.USERNAME: self.username, UsersTable.PASSWORDS: passwords})
            json.dump(table_data, table, indent=JSON_INDENT)

    def load(self, login_site: str) -> List[str]:
        try:
            with open(os.path.join(BASE_DIR, UsersTable.USERS_TABLE_FILENAME), WRITE_MODE) as table:
                table_data = json.load(table)
                encrypted_login_site = encrypt(login_site.encode(), self.master_key)
                return self._decrypt_login_details(table_data[self.username][encrypted_login_site])
        except KeyError:
            raise LoginSiteNotExists("Unregistered login site.")

    def verify(self) -> None:
        with open(os.path.join(BASE_DIR, UsersTable.USERS_TABLE_FILENAME), WRITE_MODE) as table:
            table_data = json.load(table)
            if self.username not in table_data:
                raise UnregisteredUser(f"The username {self.username} is unregistered.")
            dummy_login_site = list(table_data[self.username])[0]
            # if the password is wrong, should raise InvalidToken exception
            decrypt(dummy_login_site, self.master_key)

    def get_login_sites(self) -> List[str]:
        with open(os.path.join(BASE_DIR, UsersTable.USERS_TABLE_FILENAME), WRITE_MODE) as table:
            table_data = json.load(table)
            return list(set(self._decrypt_login_details(table_data[self.username].keys())))

    def get_login_passwords(self) ->List[str]:
        with open(os.path.join(BASE_DIR, UsersTable.USERS_TABLE_FILENAME), WRITE_MODE) as table:
            table_data = json.load(table)
            return list(set(self._decrypt_login_details([login_details[1] for login_details in
                                                         table_data[self.username].values()])))

    def _generate_dummy_login_details(self) -> List[str]:
        # dummy login_site, dummy login_username, dummy password
        return [UsersTable._generate_random_string(),
                UsersTable._generate_random_string(),
                UsersTable._generate_random_string()]

    @staticmethod
    def _generate_random_string() -> str:
        return ''.join(random.choices(string.ascii_uppercase + string.digits,
                                      k=UsersTable.DUMMY_LENGTH))

    def _encrypt_login_details(self, login_details: List[str]) -> List[str]:
        return [encrypt(detail.encode(), self.master_key).decode() for detail in login_details]

    def _decrypt_login_details(self, login_details: List[str]) -> List[str]:
        return [decrypt(detail, self.master_key).decode() for detail in login_details]

    @staticmethod
    def _arrange_login_details(login_details: List[str]) -> Dict[str, List[str]]:
        return {login_details[0]: [login_details[1], [login_details[2]]]}
