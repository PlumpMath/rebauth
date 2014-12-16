from socketserver import BaseRequestHandler
from threading import current_thread,main_thread
from Enum import SocketEnum

class ClientSocket(BaseRequestHandler):
  _PIN=b''
  _lastFN=None
  def __init__(self):
    super().__init__()
    #ACK,PIN,SCAN,SCAN_ANS,MASTER_LOC_IPV4,MASTER_LOC_IPV6,SHAKEHAND,SHAKE_SUCC,SYNC_FETCH,SYNC_PULL,EXCHANGE_PVG=range(11)
    self._codeLst = ((self._ack,),(self._givePIN,2),(self._scan,),(self._scanAns,),(self._masterloc,),(self._masterloc,),(self._shakehand,),(self._shakesucc,),(self._syncFetch,4),(self._syncPull,4),(self._exchangePVG,))
  def setup(self):
    self.server.connected(self)
  def handle(self):
    msg = self.request.recv()
    if len(msg)<1 or not msg[0].isdigit(): return
    print(current_thread().getName(),'-', self.client_address, ':', msg)
    # for enum in SocketEnum:
    self._lastFN=fnNum=int(msg[0])
    if 0 <= fnNum < len(self._codeLst):
      code = self._codeLst[fnNum]
      fn,arg,ind = code[0],[],1
      for i in range(1,len(code)):
        if ind+code[i]>=len(msg) : break
        arg.append(msg[ind:ind+code[i]])
        ind+=code[i]
      if len(msg) > ind:
        arg.append(msg[ind:])
      fn(*arg)
  def _ack(self, msg=b''):
    if self._lastFN is None or self._lastFN == SocketEnum.ACK.value: return
    self.request.sendall(int.to_bytes(SocketEnum.ACK.value, 1, 'big'))
  def _givePIN(self, PIN = b''):
    self.server.connected(self, int(PIN) if PIN.isdigit() else 0)
  def _scan(self):pass
  def _scanAns(self):pass
  def _masterloc(self):pass
  def _masterloc(self):pass
  def _shakehand(self):pass
  def _shakesucc(self):pass
  def _syncFetch(self,urlLen,url):
    if len(url)!=urlLen: return
    self.server.db.executeQuery('select * from Tactics')
  def _syncPull(self):pass
  def _exchangePVG(self):pass
  def finish(self):
    self.server.disconnected(self)
  def getPIN(self):
    return self._PIN