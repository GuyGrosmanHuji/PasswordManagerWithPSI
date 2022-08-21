from typing import Optional, List, Tuple

from Client.ClientBackend.users_table import UsersTable


class ClientBackend:
    def __init__(self):
        self.users_table = UsersTable()

    def register_user(self, username: str, password: str):
        self.users_table.register(username, password)

    def verify_user(self, username: str, password: str):
        self.users_table.verify(username, password)

    def write_login_details(self,
                            login_details: Optional[List[str], Tuple[str]],
                            mode: str) -> None:
        self.users_table.save(login_details, mode)

    def delete_login_details(self, login_site: str) -> None:
        self.users_table.delete(login_site)

    def load_login_details(self, login_site: str) -> List[str]:
        return self.users_table.load(login_site)

    def retrieve_all_login_sites(self) -> List[str]:
        return self.users_table.get_login_sites()

    def retrieve_hashed_passwords(self) -> List[int]:
        return self.users_table.get_hashed_login_passwords()
