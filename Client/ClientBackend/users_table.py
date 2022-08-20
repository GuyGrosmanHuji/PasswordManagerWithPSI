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

    BASE_DIR = os.path.dirname(__file__)

    JSON_INDENT = 4

    FILE_MODE = 'r+'

    EMPTY_STR = ""

    def __init__(self):
        if not os.path.isfile(os.path.join(BASE_DIR, UsersTable.USERS_TABLE_FILENAME)):
            with open(os.path.join(BASE_DIR, UsersTable.USERS_TABLE_FILENAME),
                      UsersTable.FILE_MODE) as login_json:
                json.dump((), login_json, indent=JSON_INDENT)
        self.username = UsersTable.EMPTY_STR
        self.master_key = UsersTable.EMPTY_STR

    def register(self, username: str, password: str) -> None:
        with open(os.path.join(BASE_DIR, UsersTable.USERS_TABLE_FILENAME), UsersTable.FILE_MODE) \
                as users_table:
            users_table_data = json.load(users_table)
            if self.username in users_table_data.keys():
                raise UnavailableUsername("This username is unavailable.")
            self.username = username
            self.master_key = generate_key(password)
            login_details = self._generate_dummy_login_details()
            encrypted_login_details = self._encrypt_login_details(login_details)
            encrypted_login_details = UsersTable._arrange_login_details(encrypted_login_details)
            users_table_data[self.username] = {}
            passwords = users_table_data[self.username].update(encrypted_login_details)
            users_table_data.update({UsersTable.USERNAME: self.username,
                                     UsersTable.PASSWORDS: passwords})
            json.dump(users_table_data, users_table, indent=JSON_INDENT)

    def save(self, login_details: Union[List[str], Tuple[str]]) -> None:
        with open(os.path.join(BASE_DIR, UsersTable.USERS_TABLE_FILENAME), UsersTable.FILE_MODE) \
                as users_table:
            users_table_data = json.load(users_table)
            encrypted_login_details = self._encrypt_login_details(login_details)
            encrypted_login_details = UsersTable._arrange_login_details(encrypted_login_details)
            passwords = users_table_data[self.username].update(encrypted_login_details)
            users_table_data.update({UsersTable.USERNAME: self.username,
                                     UsersTable.PASSWORDS: passwords})
            json.dump(users_table_data, users_table, indent=JSON_INDENT)

    def load(self, login_site: str) -> List[str]:
        try:
            with open(os.path.join(BASE_DIR, UsersTable.USERS_TABLE_FILENAME),
                      UsersTable.FILE_MODE) \
                    as users_table:
                users_table_data = json.load(users_table)
                encrypted_login_site = encrypt(login_site.encode(), self.master_key)
                return self._decrypt_login_details(users_table_data[self.username]
                                                   [encrypted_login_site])
        except KeyError:
            raise LoginSiteNotExists("Unregistered login site.")

    def verify(self, username: str, password: str) -> None:
        with open(os.path.join(BASE_DIR, UsersTable.USERS_TABLE_FILENAME), UsersTable.FILE_MODE) \
                as \
                users_table:
            users_table_data = json.load(users_table)
            if self.username not in users_table_data:
                raise UnregisteredUser(f"The username {self.username} is unregistered.")
            self.username = username
            self.master_key = generate_key(password)
            dummy_login_site = list(users_table_data[self.username])[0]
            # if the password is wrong, should raise InvalidToken exception
            try:
                decrypt(dummy_login_site, self.master_key)
            except:
                raise WrongPassword("Wrong password.")

    def get_login_sites(self) -> List[str]:
        with open(os.path.join(BASE_DIR, UsersTable.USERS_TABLE_FILENAME), UsersTable.FILE_MODE) \
                as \
                users_table:
            users_table_data = json.load(users_table)
            return list(set(self._decrypt_login_details(users_table_data[self.username].keys())))

    def get_login_passwords(self) -> List[str]:
        with open(os.path.join(BASE_DIR, UsersTable.USERS_TABLE_FILENAME), UsersTable.FILE_MODE) \
                as users_table:
            users_table_data = json.load(users_table)
            return list(set(self._decrypt_login_details([login_details[1] for login_details in
                                                         users_table_data[self.username]
                                                        .values()])))

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
