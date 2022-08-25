from Communication.params import SERVER_IP, SERVER_PORT
from Communication.tools import SocketFacade
from Crypto.PSI.server_side_psi import *
from Server.ServerBackend.passwordstable import PasswordsTable


class ServerBackend:
    def __init__(self):
        self.updated = False
        self.passwords_table = PasswordsTable()
        self.passwords = self.passwords_table.load()
        print("S1")
        self.hash_table = insert_to_hash_table(self.passwords)
        print("S2")
        self.poly_coefficients = get_poly_coefficients(self.hash_table)
        print("S3")

    def run(self):
        """
        Waits for PSI Protocol queries
        """
        while True:
            with SocketFacade(listen_to=(SERVER_IP, SERVER_PORT)) as s:
                query = s.get_msg()
                if query == b'STOP':
                    print("SERVER: Goodbye!")
                    break
                encrypted_client_query = deserialize_client_powers(query)
                client_powers_vector = calculate_encrypted_powers(encrypted_client_query)
                response = get_server_response(client_powers_vector, self.poly_coefficients)
                s.send_msg(response)

    def update(self, new_passwords: List[str]):
        # TODO implement multi-threading for updating self.hash_table and self.poly_coefficients
        self.passwords += new_passwords
        self.passwords_table.save(self.passwords)
        self.updated = True
