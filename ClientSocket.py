from socketserver import BaseRequestHandler
from threading import current_thread,main_thread
from Enum import SocketEnum
class ClientSocket(BaseRequestHandler):
  _PIN=b''
  def __init__(self):
    super().__init__()
  def handle(self):
    print(current_thread().getName(), self.client_address, ':', self.request.recv(1024))
  def setup(self):
    self.server.db.executeQuery('insert into ')
    self.request.sendall(int.to_bytes(SocketEnum.PIN.value, 1, 'big') + b'')
    self.server.socketList.append(self)
  def finish(self):
    self.server.socketList.remove(self)
  def getPIN(self):
    return self._PIN