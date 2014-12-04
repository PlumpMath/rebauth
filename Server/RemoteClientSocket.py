from socketserver import TCPServer, BaseRequestHandler
from ClientSocket import ClientSocket

class REmoteClientSocket(ClientSocket):
  _clientAddress=''
  def listen(self):
    pass
  def _servLocalClient(self):
    pass
  def close(self):
    pass