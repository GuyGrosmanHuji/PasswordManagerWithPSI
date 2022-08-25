import socket
import time
from typing import Union, Tuple, Optional
from Communication.params import *
from Communication.exceptions import *

CommDetails = Tuple[str, int]   # (ip, port)

class SocketFacade:
    """
    Wraps the socket class for simpler communication
    """
    def __init__(self,
                 listen_to: Optional[CommDetails] = None,
                 connect_to: Optional[CommDetails] = None
                 ):
        self.socket: Optional[socket.socket] = None
        self.conn: Optional[socket.socket] = None
        self.connect_to = connect_to
        self.listen_to = listen_to

    @staticmethod
    def _fix_msg(msg: Union[str, bytes]) -> bytes:
        if type(msg) is str:
            msg = msg.encode()
        return msg

    def _choose_socket(self):
        s = self.conn if self.conn else self.socket
        if not s:
            raise SocketIsNotConnected("Use this method only within 'with' scope")
        return s

    def send_msg(self, msg: Union[str, bytes]):
        msg = self._fix_msg(msg)
        s = self._choose_socket()
        length_msg = f'{len(msg)}{FILLER * (RECV_LENGTH - len(msg))}'
        s.sendall(length_msg.encode())
        time.sleep(0.5)
        s.sendall(msg)

    def get_msg(self) -> bytes:
        s = self._choose_socket()
        msg_len = s.recv(RECV_LENGTH).decode().strip()
        msg_len = int(msg_len, base=10)
        full_msg = b''
        while len(full_msg) < msg_len:
            msg = s.recv(MSG_LENGTH)
            if not msg:
                break
            full_msg += msg
        return full_msg

    def __enter__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if self.connect_to:
            self.socket.connect(self.connect_to)

        elif self.listen_to:
            self.socket.bind(self.listen_to)
            self.socket.listen()
            self.conn, _ = self.socket.accept()
        return self

    def __exit__(self, *args):
        if self.conn:
            self.conn.close()
            self.conn = None
        self.socket.close()
        self.socket = None
