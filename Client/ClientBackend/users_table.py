import os
import json
import random
import string

from typing import Union, Dict, List, Tuple

from Client.ClientBackend.exceptions import *

from Crypto.crypto import *


class UsersTable:
    USERS_TABLE_FILENAME = "users_table.json"
    USERNAME = "username"
    PASSWORDS = "passwords"
    LOGIN_SITE = "login_site"
    LOGIN_USERNAME = "login_username"
    LOGIN_PASSWORD = "login_password"

    DUMMY_LENGTH = 16

    SITE_IDX = 0
    USERNAME_IDX = 1
    PASSWORD_IDX = 2

    BASE_DIR = os.path.dirname(__file__)
    JSON_INDENT = 4
    FILE_READ_WRITE_MODE = 'r+'
    FILE_WRITE_MODE = 'w'
    FILE_BEGIN = 0

    EMPTY_STR = ""
    EMPTY_BYTES = EMPTY_STR.encode()

    ADD_MODE = "add"
    EDIT_MODE = "edit"

    def __init__(self):
        if not os.path.isfile(os.path.join(UsersTable.BASE_DIR, UsersTable.USERS_TABLE_FILENAME)):
            with open(os.path.join(UsersTable.BASE_DIR, UsersTable.USERS_TABLE_FILENAME),
                      UsersTable.FILE_WRITE_MODE) as login_json:
                json.dump({}, login_json, indent=UsersTable.JSON_INDENT)
        self.username = UsersTable.EMPTY_STR
        self.master_key = UsersTable.EMPTY_STR

    def register(self, username: str, password: str) -> None:
        with open(os.path.join(UsersTable.BASE_DIR, UsersTable.USERS_TABLE_FILENAME),
                  UsersTable.FILE_READ_WRITE_MODE) as users_table:
            users_table_data = json.load(users_table)

            # initialize username
            self.username = username

            if self.username in users_table_data.keys():
                raise UnavailableUsername("This username is unavailable.")

            # initialize master_key
            self.master_key = generate_key(password)

            dummy_details = self._generate_dummy_login_details()
            encrypted_dummy_details = self._encrypt_login_details(dummy_details)
            encrypted_login_details = UsersTable._arrange_login_details(encrypted_dummy_details)
            users_table_data[self.username] = encrypted_login_details
            users_table.seek(UsersTable.FILE_BEGIN)
            json.dump(users_table_data, users_table, indent=UsersTable.JSON_INDENT)
            users_table.truncate()

    def write(self, login_details: Union[List[str], Tuple[str]], mode: str = "add") -> None:
        with open(os.path.join(UsersTable.BASE_DIR, UsersTable.USERS_TABLE_FILENAME),
                  UsersTable.FILE_READ_WRITE_MODE) as users_table:
            users_table_data = json.load(users_table)

            encrypted_login_details = self._encrypt_login_details(login_details)

            if mode == UsersTable.EDIT_MODE:
                if not encrypted_login_details[UsersTable.SITE_IDX] in \
                       users_table_data[self.username]:
                    raise UnregisteredLoginSite(f"The login site"
                                                f" {login_details[UsersTable.SITE_IDX]} is "
                                                f"unregistered.")

            encrypted_login_details = UsersTable._arrange_login_details(encrypted_login_details)
            all_encrypted_login_details = users_table_data[self.username]
            all_encrypted_login_details.update(encrypted_login_details)
            users_table_data[self.username] = all_encrypted_login_details
            users_table.seek(UsersTable.FILE_BEGIN)
            json.dump(users_table_data, users_table, indent=UsersTable.JSON_INDENT)
            users_table.truncate()

    def delete(self, login_site: str) -> None:
        with open(os.path.join(UsersTable.BASE_DIR, UsersTable.USERS_TABLE_FILENAME),
                  UsersTable.FILE_READ_WRITE_MODE) as users_table:
            try:
                users_table_data = json.load(users_table)

                encrypted_login_site = encrypt(login_site, self.master_key)
                del users_table_data[self.username][encrypted_login_site]

                users_table.seek(UsersTable.FILE_BEGIN)
                json.dump(users_table_data, users_table, indent=UsersTable.JSON_INDENT)
                users_table.truncate()

            except KeyError:
                raise UnregisteredLoginSite(f"The login site {login_site} is unregistered.")

    def load(self, login_site: str) -> List[str]:
        with open(os.path.join(UsersTable.BASE_DIR, UsersTable.USERS_TABLE_FILENAME),
                  UsersTable.FILE_READ_WRITE_MODE) as users_table:
            try:
                users_table_data = json.load(users_table)

                encrypted_login_site = encrypt(login_site, self.master_key)

                # returns decrypted login username, decrypted login password
                return self._decrypt_login_details(
                    users_table_data[self.username][encrypted_login_site])
            except KeyError:
                raise UnregisteredLoginSite(f"The login site{login_site} is unregistered.")

    def verify(self, username: str, password: str) -> None:
        with open(os.path.join(UsersTable.BASE_DIR, UsersTable.USERS_TABLE_FILENAME),
                  UsersTable.FILE_READ_WRITE_MODE) as users_table:
            users_table_data = json.load(users_table)

            if self.username not in users_table_data:
                raise UnregisteredUser(f"The username {self.username} does not exist.")

            # initialize username and master_key here
            self.username = username
            self.master_key = generate_key(password)

            # convert dictionary of login details of users to list: take the first element from
            # there which is dummy login details, and take the first element in the tuple which
            # is the encrypted dummy login site
            dummy_login_site = list(users_table_data[self.username])[0][UsersTable.SITE_IDX]

            # if the password is wrong, should raise InvalidToken exception
            try:
                decrypt(dummy_login_site, self.master_key)
            except:
                raise WrongPassword("Wrong password.")

    def get_login_sites(self) -> List[str]:
        with open(os.path.join(UsersTable.BASE_DIR, UsersTable.USERS_TABLE_FILENAME),
                  UsersTable.FILE_READ_WRITE_MODE) as users_table:
            users_table_data = json.load(users_table)
            return [decrypt(login_site, self.master_key) for login_site in
                    users_table_data[self.username]]

    def get_hashed_login_passwords(self) -> List[int]:
        with open(os.path.join(UsersTable.BASE_DIR, UsersTable.USERS_TABLE_FILENAME),
                  UsersTable.FILE_READ_WRITE_MODE) as users_table:
            users_table_data = json.load(users_table)
            decrypted_passwords = list(set(self._decrypt_login_details(
                [login_details[1] for login_details in users_table_data[self.username].values()])))
            hash_passwords = [hash_password(password) for password in decrypted_passwords]
            return hash_passwords

    def get_login_sites_by_passwords(self, passwords):
        with open(os.path.join(UsersTable.BASE_DIR, UsersTable.USERS_TABLE_FILENAME),
                  UsersTable.FILE_READ_WRITE_MODE) as users_table:
            users_table_data = json.load(users_table)
            user_table_data = users_table_data[self.username]
            return [decrypt(login_site, self.master_key) for login_site, login_values in
                    user_table_data if self._decrypt_login_details([login_site, *login_values])[
                        UsersTable.PASSWORD_IDX] in passwords]

    def _generate_dummy_login_details(self) -> List[str]:
        # dummy login_site, dummy login_username, dummy password
        return [UsersTable._generate_random_string(),
                UsersTable._generate_random_string(),
                UsersTable._generate_random_string()]

    def _encrypt_login_details(self, login_details: Union[List[str], Tuple[str]]) -> List[str]:
        return [encrypt(detail, self.master_key) for detail in login_details]

    def _decrypt_login_details(self, login_details: Union[List[str], Tuple[str]]) -> List[str]:
        return [decrypt(detail, self.master_key) for detail in login_details]

    @staticmethod
    def _generate_random_string() -> str:
        return ''.join(random.choices(string.ascii_uppercase + string.digits,
                                      k=UsersTable.DUMMY_LENGTH))

    @staticmethod
    def _arrange_login_details(login_details: List[str]) -> Dict[str, List[str]]:
        return {login_details[UsersTable.SITE_IDX]: [login_details[UsersTable.USERNAME_IDX],
                                                     login_details[UsersTable.PASSWORD_IDX]]}
