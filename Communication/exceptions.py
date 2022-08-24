class SocketIsNotConnected(Exception):
    def __init__(self, message, cause=None):
        super(SocketIsNotConnected, self).__init__(message)
        self._cause = cause
