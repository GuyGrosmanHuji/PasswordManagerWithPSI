from typing import Any
from threading import Thread

from Communication.params import SERVER_IP, SERVER_PORT
from Communication.utils import SocketFacade
from Crypto.PSI.server_side_psi import *
from Server.ServerBackend.passwordstable import PasswordsTable


class ServerBackend:
    def __init__(self):
        self.updated = False
        self.passwords_table = PasswordsTable()
        self.passwords = self.passwords_table.load()
        print("SERVER: Hashing data set...")
        self.hash_table = insert_to_hash_table(self.passwords)
        print("SERVER: Calculating polynomial...")
        self.poly_coefficients = get_poly_coefficients(self.hash_table)

    def run(self):
        """
        Waits for PSI Protocol queries
        """
        while True:
            update_struct = [False]
            if self.updated:
                updating_thread = Thread(target=self.update_psi_objects, args=(update_struct,))
                updating_thread.run()
            with SocketFacade(listen_to=(SERVER_IP, SERVER_PORT)) as s:
                query = s.get_msg()
                if query == b'STOP':
                    print("SERVER: Goodbye!")
                    break
                encrypted_client_query = deserialize_client_powers(query)
                client_powers_vector = calculate_encrypted_powers(encrypted_client_query)
                response = get_server_response(client_powers_vector, self.poly_coefficients)
                s.send_msg(response)
            if update_struct[0]:
                self.hash_table, self.poly_coefficients = update_struct[0]
                update_struct[0] = False

    def update_psi_objects(self, results: List[Any]):
        hash_table = insert_to_hash_table(self.passwords, False)
        poly_coefficients = get_poly_coefficients(self.hash_table, False)
        results[0] = (hash_table, poly_coefficients)
        self.updated = False

    def update(self, new_passwords: List[str]):
        self.passwords += new_passwords
        self.passwords_table.save(self.passwords)
        self.updated = True
