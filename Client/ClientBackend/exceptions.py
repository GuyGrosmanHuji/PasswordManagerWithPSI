class UnavailableUsername(Exception):
    def __init__(self, message, cause=None):
        super(UnavailableUsername, self).__init__(message)
        self._cause = cause


class UnregisteredUser(Exception):
    def __init__(self, message, cause=None):
        super(UnregisteredUser, self).__init__(message)
        self._cause = cause


class WrongPassword(Exception):
    def __init__(self, message, cause=None):
        super(WrongPassword, self).__init__(message)
        self._cause = cause


class UnregisteredLoginSite(Exception):
    def __init__(self, message, cause=None):
        super(UnregisteredLoginSite, self).__init__(message)
        self._cause = cause
