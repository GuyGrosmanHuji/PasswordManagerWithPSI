from typing import Union, List, Tuple

from Client.ClientBackend.users_table import UsersTable
import Crypto.PSI.client_side_psi as cs_psi
from Crypto.PSI.tools import get_context
import Communication.params as comm
from Communication.tools import SocketFacade

class ClientBackend:
    def __init__(self):
        self.users_table = UsersTable()
        self.context = get_context()        # SEAL homomorphic encryption context
        self.cuckoo = None
        self.window = None
        self.is_updated = True

    def register_user(self, username: str, password: str):
        self.users_table.register(username, password)

    def verify_user(self, username: str, password: str):
        self.users_table.verify(username, password)

    def write_login_details(self,
                            login_details: Union[List[str], Tuple[str]],
                            mode: str) -> None:
        self.users_table.write(login_details, mode)
        self.is_updated = True

    def delete_login_details(self, login_site: str) -> None:
        self.users_table.delete(login_site)
        self.is_updated = True

    def load_login_details(self, login_site: str) -> List[str]:
        return self.users_table.load(login_site)

    def retrieve_compromised_login_sites(self, leaked_passwords):
        return self.users_table.get_login_sites_by_passwords(leaked_passwords)

    def retrieve_all_login_sites(self) -> List[str]:
        return self.users_table.get_login_sites()

    def psi_protocol(self) -> List[str]:
        """
        Returns a list of all the leaked passwords
        """
        # Offline pre-processing: performs windowing to the passwords and
        if self.is_updated:
            logged_in_passwords = self.users_table.get_all_login_passwords()
            self.cuckoo = cs_psi.get_cuckoo_items(logged_in_passwords)
            self.window = cs_psi.get_windowing_tensor(self.cuckoo)
            self.is_updated = False
        enc_msg = cs_psi.prepare_encrypted_message(self.window, self.context)
        # Online process - send query to server and get response:
        with SocketFacade(connect_to=(comm.SERVER_IP, comm.SERVER_PORT)) as s:
            s.send_msg(enc_msg)
            server_feedback = s.get_msg()

        # Offline post-process: intersection calculation procedure:
        dec_server_feedback = cs_psi.decrypt_server_answer(server_feedback, self.context)
        intersection = cs_psi.find_intersection(dec_server_feedback, self.cuckoo)
        print(intersection)
        return self.retrieve_compromised_login_sites(list(intersection))
