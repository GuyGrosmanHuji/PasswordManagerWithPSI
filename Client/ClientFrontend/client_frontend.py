import pyperclip
from pwinput import pwinput

from Client.ClientBackend.client_backend import ClientBackend
from Client.ClientFrontend.inputs import *
from Client.ClientFrontend.messages import *

cls = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
# cls = lambda: print()


class ClientFrontend:
    QUIT_SIGNAL: int = 0
    CONT_SIGNAL: int = 1
    BAD_LOG_IN_SIGNAL: int = 2

    def __init__(self):
        self.client_backend = ClientBackend()

    def run(self):
        cls()
        print(BIG_TITLE)
        while True:
            sig = self._login_screen()
            while sig == ClientFrontend.BAD_LOG_IN_SIGNAL:
                sig = self._login_screen()
            if not sig: break
            sig = self._main_screen()
            if not sig: break
        print(GOODBYE_MSG)

    def _login_screen(self) -> int:
        print(WELCOME_MSG)
        print(LOGIN_OPTS_MSG)
        opt = input()
        while opt not in LOGIN_OPTS:
            print(INVALID_INPUT_MSG)
            print(LOGIN_OPTS_MSG)
            opt = input()
        if opt == LOG_IN_QUIT_OPT:
            return ClientFrontend.QUIT_SIGNAL
        try:
            username = input(USERNAME_MSG)
            if opt == SIGN_UP_OPT:
                self._sign_up_screen(username=username)
            elif opt == SIGN_IN_OPT:
                self._sign_in_screen(username=username)
            return ClientFrontend.CONT_SIGNAL
        except Exception as e:
            print(ERROR_PREFIX + str(e))
            print()
            return ClientFrontend.BAD_LOG_IN_SIGNAL

    def _main_screen(self):
        while True:
            cls()
            print(MAIN_OPTS_MSG)
            opt = input()
            while opt not in MAIN_OPTS:
                print(INVALID_INPUT_MSG)
                print(MAIN_OPTS_MSG)
                opt = input()
            try:
                if opt == ADD_LOG_DETAILS_OPT:
                    self._write_login_details(mode="add")
                elif opt == EDIT_LOG_DETAILS_OPT:
                    self._write_login_details(mode="edit")
                elif opt == DELETE_LOG_DETAILS_OPT:
                    self._delete_login_details()
                elif opt == RETRIEVE_LOG_DETAILS_OPT:
                    self._retrieve_login_details()
                elif opt == CHECK_LOG_DETAILS_LEAKAGE_OPT:
                    self._check_login_details_leakage()
                elif opt == RETRIEVE_ALL_LOG_DETAILS_OPT:
                    self._retrieve_all_login_sites()
                elif opt == LOG_OUT_OPT:
                    return ClientFrontend.CONT_SIGNAL
                elif opt == MAIN_SCREEN_QUIT_OPT:
                    return ClientFrontend.QUIT_SIGNAL
            except Exception as e:
                print(ERROR_PREFIX + str(e))
            finally:
                self._continue_screen()

    def _sign_up_screen(self, username: str):
        while True:
            password = pwinput(prompt=PASSWORD_MSG)
            repeat_password = pwinput(prompt=REPEAT_PASSWORD_MSG)
            if password == repeat_password:
                break
            else:
                print(NOT_MATCHING_PASSWORD_MSG)
        self.client_backend.register_user(username, password)

    def _sign_in_screen(self, username: str):
        password = pwinput(prompt=PASSWORD_MSG)
        self.client_backend.verify_user(username, password)

    def _psi(self):
        # TODO: print it nicely
        compromised_websites = self.client_backend.psi_protocol()
        return compromised_websites

    def _write_login_details(self, mode: str):
        login_site = input(SITE_MSG)
        login_username = input(USERNAME_MSG)
        login_password = pwinput(prompt=PASSWORD_MSG)
        self.client_backend.write_login_details([login_site, login_username, login_password], mode)

    def _delete_login_details(self):
        login_site = input(SITE_MSG)
        self.client_backend.delete_login_details(login_site)
        print(f"{login_site}" + DELETE_COMPLETED_MSG)

    def _retrieve_login_details(self):
        login_site = input(SITE_MSG)
        login_username, login_password = \
            self.client_backend.load_login_details(login_site)
        print(RETRIEVED_INFO_MSG)
        print(USERNAME_MSG + login_username)
        pyperclip.copy(login_password)
        print(PASSWORD_COPY_MSG)

    def _check_login_details_leakage(self):
        # expecting to get list (empty or more elements) with all the login sites that are
        # compromised
        leaked_passwords = self._psi()
        if leaked_passwords:
            print(LEAKAGE_MSG)
            compromised_login_sites = self.client_backend.retrieve_compromised_login_sites(
                leaked_passwords)
            print('\n'.join(compromised_login_sites))
            print()

    def _retrieve_all_login_sites(self):
        login_sites = self.client_backend.retrieve_all_login_sites()
        print(RETRIEVED_INFO_MSG)
        print('\n'.join(login_sites))

    def _continue_screen(self):
        ans = input(PRESS_ENTER_MSG)
        while ans != "":
            ans = input(PRESS_ENTER_MSG)


if __name__ == '__main__':
    cf = ClientFrontend()
    cf.run()
