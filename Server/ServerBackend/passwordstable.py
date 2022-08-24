import json
import os
import sys


class PasswordsTable:
    WORK_DIR = os.getcwd()
    PASSWORDS_FILENAME = os.path.join(WORK_DIR, "passwords.json")
    READ_MODE = 'r'

    def load(self):
        with open(PasswordsTable.PASSWORDS_FILENAME, PasswordsTable.READ_MODE) as passwords_table:
            passwords_data = json.load(passwords_table)
            pw_hashes = list(passwords_data.values())
            passwords_mappings = self._map_passwords(pw_hashes)
        return passwords_mappings

    @staticmethod
    def _map_passwords(pw_hashes):
        return [int.from_bytes(bytes.fromhex(pw_hash)[0:4], byteorder=sys.byteorder) for pw_hash in
                pw_hashes]
