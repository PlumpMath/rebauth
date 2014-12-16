from socketserver import ThreadingTCPServer as Server
from threading import Thread
from ClientSocket import ClientSocket
from Enum import PortEnum, SocketEnum
from random import choice

class ClientSocketPool(Server):
  _masterList = []
  def __init__(self, port, db):
    try:
      super().__init__(('0.0.0.0', port), ClientSocket)
    except:
      super().__init__(('0.0.0.0', port+1), ClientSocket)
    self._servThread = Thread(target=self.serve_forever)
    self._servThread.start()
    self._port,self.db = port, db
  def removeMaster(self, PIN):
    for soc in self._masterList:
      if soc.getPIN() == PIN :
        self._masterList.remove(soc)
        return
  def searchMaster(self, PIN):
    for soc in self._masterList:
      if soc.getPIN() == PIN: return True
    return False
  def connected(self, socket, PIN = 0):
    if socket in self._masterList: return
    self._masterList.append(socket)
    if self._port == PortEnum.MAIN_SERVER:
      if not PIN or not self.searchMaster(PIN):
        min,max=10**3,10**4-1 # pin generation
        if len(self._masterList) >= 1 + max - min:
          print('PIN number needs to be bigger')
          exit(1)
        blackset = {soc.getPIN() for soc in self._masterList}
        whiteset = set(range(min,max + 1))
        PIN = choice(list(whiteset.difference(blackset)))
        del whiteset, blackset
      socket.request.sendall(int.to_bytes(SocketEnum.PIN.value, 1, 'big') + int.to_bytes(PIN, 2, 'big'))
    else:
      # shakehand
      pass
  def disconnected(self, socket):
    self._masterList.remove(self)