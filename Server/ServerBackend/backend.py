from Server.ServerBackend.passwordstable import PasswordsTable

class Backend:
    def __init__(self):
        self.passwords_table = PasswordsTable()

    def get_passwords(self):
        return self.passwords_table.load()