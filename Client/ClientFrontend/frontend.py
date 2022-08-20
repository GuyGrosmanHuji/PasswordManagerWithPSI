import sys

# TODO change the names of the classes for separation
from Client.ClientBackend.backend import ClientBackend
from Server.ServerBackend.backend import ServerBackend

from Client.ClientFrontend.messages import *
from Client.ClientFrontend.inputs import *

class Frontend:
    SIGN_UP_MODE = "sign-up"
    SIGN_IN_MODE = "sign-in"

    def __init__(self):
        self.client_backend : ClientBackend
        self.server_backend : ServerBackend

    def run(self):
        print(WELCOME_MSG)
        while True:
            print(LOG_IN_OPTS_MSG)
            opt = input()
            while opt not in LOG_IN_OPTS:
                print(INVALID_INPUT_MSG)
                print(LOG_IN_OPTS_MSG)
            try:
                username = input(USERNAME_MSG)
                password = input(PASSWORD_MSG)
                mode = Frontend.SIGN_UP_MODE if opt in SIGN_UP_OPT else Frontend.SIGN_IN_MODE
            except Exception as e:
                print(e)
