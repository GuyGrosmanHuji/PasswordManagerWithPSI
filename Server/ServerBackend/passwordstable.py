import os


class PasswordsTable:
    WORK_DIR = os.getcwd()
    PASSWORDS_FILENAME = os.path.join(WORK_DIR, "passwords.txt")
    READ_MODE = 'r'

    def load(self):
        with open(PasswordsTable.PASSWORDS_FILENAME, PasswordsTable.READ_MODE) as f:
            passwords = f.readlines()
            # TODO if we work with bytes convert to bytes; if we work with string keep as is
            # passwords = [bytes.fromhex(password) for password in passwords]
            return passwords
