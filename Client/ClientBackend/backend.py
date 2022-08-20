from typing import Optional, List, Tuple

from Client.ClientBackend.users_table import UsersTable


class Backend:
    def __init__(self, username: str, password: str):
        # TODO if there is an exception during the creation of UsersTable, we should catch in the
        #  client's frontend
        self.users_table = UsersTable(username, password)

    def write_login_details(self, login_details: Optional[List[str], Tuple[str]]) -> None:
        self.users_table.save(login_details)

    def load_login_details(self, login_site: str) -> List[str]:
        return self.users_table.load(login_site)

    def retrieve_all_login_sites(self) -> List[str]:
        return self.users_table.get_login_sites()

    def retrieve_all_login_passwords(self) -> List[str]:
        return self.users_table.get_login_passwords()
