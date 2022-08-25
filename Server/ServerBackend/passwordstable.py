import json
import os
import sys

from typing import Union, List


class PasswordsTable:
    WORK_DIR = os.getcwd()
    PASSWORDS_FILENAME = os.path.join(WORK_DIR, "passwords.json")
    READ_MODE = 'r'

    def load(self):
        with open(PasswordsTable.PASSWORDS_FILENAME, PasswordsTable.READ_MODE) as passwords_table:
            passwords_data = json.load(passwords_table)
        return passwords_data

    def save(self, passwords):
        with open(PasswordsTable.PASSWORDS_FILENAME, PasswordsTable.READ_MODE) as passwords_table:
            json.dump(passwords_table, passwords)
            passwords_table.truncate()


    @staticmethod
    def _map_passwords(pw_hashes):
        return [int.from_bytes(bytes.fromhex(pw_hash)[0:4], byteorder=sys.byteorder) for pw_hash in
                pw_hashes]
