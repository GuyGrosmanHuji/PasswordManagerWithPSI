import json
import os
import sys


class PasswordsTable:
    WORK_DIR = os.getcwd()
    PASSWORDS_FILENAME = os.path.join(WORK_DIR, "Server", "ServerBackend", "passwords.json")
    READ_MODE = 'r'

    @staticmethod
    def load():
        with open(PasswordsTable.PASSWORDS_FILENAME, PasswordsTable.READ_MODE) as passwords_table:
            passwords_data = json.load(passwords_table)
        return passwords_data

    @staticmethod
    def save(passwords):
        with open(PasswordsTable.PASSWORDS_FILENAME, PasswordsTable.READ_MODE) as passwords_table:
            json.dump(passwords_table, passwords)
            passwords_table.truncate()


    @staticmethod
    def _map_passwords(pw_hashes):
        return [int.from_bytes(bytes.fromhex(pw_hash)[0:4], byteorder=sys.byteorder) for pw_hash in
                pw_hashes]
