from socketserver import ThreadingTCPServer as Server
from threading import Thread
from ClientSocket import ClientSocket

class ClientSocketPool(Server):
  socketList = []
  def __init__(self,db):
    super().__init__(('0.0.0.0',39274),ClientSocket)
    self._servThread = Thread(target=self.serve_forever)
    self._servThread.start()
    self.db=db
  def searchSocket(self, PIN):
    for soc in self._socketList:
      if soc.getPIN() == PIN: return PIN
    return None