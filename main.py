import threading

import Communication.params as comm
from Communication.tools import SocketFacade
from Client.ClientFrontend.client_frontend import ClientFrontend
from Server.ServerBackend.server_backend import ServerBackend

s = ServerBackend()
server_thread = threading.Thread(target=s.run)
server_thread.start()

c = ClientFrontend()
c.run()

print("Stopping...")
# STOP SERVER:
with SocketFacade(connect_to=(comm.SERVER_IP, comm.SERVER_PORT)) as s:
    s.send_msg(b'STOP')
