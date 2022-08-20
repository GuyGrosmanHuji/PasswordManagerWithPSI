class UnregisteredUser(Exception):
    def __init__(self, message, cause=None):
        super(UnregisteredUser, self).__init__(message)
        self._cause = cause


class WrongPassword(Exception):
    def __init__(self, message, cause=None):
        super(WrongPassword, self).__init__(message)
        self._cause = cause


class LoginSiteNotExists(Exception):
    def __init__(self, message, cause=None):
        super(LoginSiteNotExists, self).__init__(message)
        self._cause = cause