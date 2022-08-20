import sys

from getpass import getpass

import pyperclip

from Client.ClientBackend.backend import ClientBackend
from Server.ServerBackend.backend import ServerBackend

from Client.ClientFrontend.messages import *
from Client.ClientFrontend.inputs import *


class Frontend:
    def __init__(self):
        self.client_backend = ClientBackend()
        self.server_backend = ServerBackend()

    def run(self):
        self._login_screen()
        self._main_screen()

    def _login_screen(self):
        print(WELCOME_MSG)
        print(LOGIN_OPTS_MSG)
        opt = input()
        while opt not in LOGIN_OPTS:
            print(INVALID_INPUT_MSG)
            print(LOGIN_OPTS_MSG)
            opt = input()
        while True:
            try:
                username = input(USERNAME_MSG)
                password = input(PASSWORD_MSG)
                if opt == SIGN_UP_OPT:
                    self.client_backend.register_user(username, password)
                elif opt == SIGN_IN_OPT:
                    self.client_backend.verify_user(username, password)
                break
            except Exception as e:
                print(ERROR_PREFIX + str(e))
        sys.stdout.flush()

    def _main_screen(self):
        # expecting to get list (empty or more elements) with all the login sites that are
        # compromised
        # TODO need to implement a method which given a compromised password know to relate
        #  it to the relevant login sites
        compromised_login_sites = self._psi()
        if compromised_login_sites:
            print(LEAKAGE_MSG)
            print('\n'.join(compromised_login_sites))
            print()
        while True:
            print(MAIN_OPTS_MSG)
            opt = input()
            while opt not in MAIN_OPTS:
                print(INVALID_INPUT_MSG)
                print(MAIN_OPTS_MSG)
                opt = input()
            try:
                if opt == ADD_LOG_DETAILS:
                    self._write_login_details(mode="add")
                elif opt == EDIT_LOG_DETAILS:
                    self._write_login_details(mode="edit")
                elif opt == DELETE_LOG_DETAILS:
                    self._delete_login_details()
                elif opt == RETRIEVE_LOG_DETAILS:
                    self._retrieve_login_details()
                elif opt == RETRIEVE_ALL_LOG_DETAILS:
                    self._retrieve_all_login_sites()
                elif opt == QUIT:
                    print(GOODBYE_MSG)
                    break
            except Exception as e:
                print(ERROR_PREFIX + str(e))
            sys.stdout.flush()

    def _psi(self):
        pass

    def _write_login_details(self, mode: str):
        login_site = input(SITE_MSG)
        login_username = input(USERNAME_MSG)
        login_password = getpass(prompt=PASSWORD_MSG, stream="*")
        self.client_backend.write_login_details(login_site, login_username, login_password, mode)

    def _delete_login_details(self):
        login_site = input(SITE_MSG)
        self.client_backend.delete_login_details(login_site)
        print(f"{login_site}" + DELETE_COMPLETED_MSG)

    def _retrieve_login_details(self):
        login_site = input(SITE_MSG)
        login_username, login_password = \
            self.client_backend.retrieve_login_details(login_site)
        print(RETRIEVED_INFO_MSG)
        print(USERNAME_MSG + login_username)
        pyperclip.copy(login_password)
        print(PASSWORD_COPY_MSG)

    def _retrieve_all_login_sites(self):
        login_sites = self.client_backend.retrieve_all_login_details()
        print(RETRIEVED_INFO_MSG)
        print('\n'.join(login_sites))
