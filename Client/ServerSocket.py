from socket import socket
from Enum import SocketEnum

class ServerSocket(socket):
  def __init__(self):
    super().__init__()
  def connect(self,mph):
    super().connect(('racu.idea.sh',39274))
    self._PIN=int.from_bytes(super().recv(3)[1:])
  def getStrategyHash(self,url,type):
    self.sendall(bytes.join(b'',map(int.to_bytes,(SocketEnum.SYNC_FETCH,8723),(1,2),('big',)*2)))
    self.recv(1)
  def getStrategy(self,url,type):

    pass
  def getCertKey(self):

    pass
  def _searchLocalArea(self):

    pass