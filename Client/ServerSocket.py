from socket import socket
from pipes import Template
from threading import Thread
from os import fstat
from os.path import join,exists
from time import sleep

from Enum import SocketEnum, IPCEnum, PortEnum
from Client.Strategy import Strategy
from Client.Tactics import Tactics

class SocketlikeIPC():
  def __init__(self, IPCpath):
    self._IPC=Template()
    self._IPCRecvPath,self._IPCSendPath=map(join,(IPCpath,)*2,('sToCPipe','cToSPipe'))
  def connect(self):  #for use
    pass
  def _connect(self): #for ACK
    self._IPCrecv=self._IPC.open_r(self._IPCRecvPath)
    self.sendall(str(IPCEnum.ACK.value))
    msg=self.recv()
    print(msg)
    if msg==str(IPCEnum.ACK.value): return True
    self._clearSend()
    self._clearRecv()
    return False
  def _clearSend(self):
    self._IPCsend=self._IPC.open_w(self._IPCSendPath)
    self._IPCsend.write('')
  def _clearRecv(self):
    self._IPC.open_w(self._IPCRecvPath).write('')
  def sendall(self, data, flags=None):
    self._clearSend()
    # self._IPCsend.seek(0)
    self._IPCsend.write(data)
    # self._IPCsend.flush()
    self._IPCsend.close()
  def recv(self, buffersize=-1, flags=None):
    msg = ''
    self._IPCrecv.seek(0)
    for i in range(1000//100):
      msg=self._IPC.open_r(self._IPCRecvPath).read(buffersize)
      if msg : break
      sleep(1.001)
    self._clearRecv()
    return msg
  def getStrategyHash(self,url,type):
    ''' :return:None on error, hash bytes on success '''
    self.sendall(str(IPCEnum.SYNC_FETCH.value) + str(type) + str(len(url)).ljust(4) + url)
    msg=''
    msg=self.recv()
    return None if msg==str(IPCEnum.ERROR.value) else bytes.fromhex(msg)
  def getStrategy(self,url,type):
    ''' :return:None on error, strategy on success '''
    self.sendall(str(IPCEnum.SYNC_PULL.value) + str(type) + str(len(url)).ljust(4) + url)
    msg=''
    msg=self.recv()
    if msg==str(IPCEnum.ERROR.value): return None
    Strategy(url,type)
  def getCertKey(self):
    pass

class ServerSocket(SocketlikeIPC, socket):
  def __init__(self,db):
    self._ipcPath=db.getSettingPath()
    super(type(self),self).__init__(self._ipcPath)
    if super(type(self),self)._connect(): return
    print('IPC failed. proceeding with TCP.')
    super(type(self)) #unbound
    super(socket,self).__init__()
    self.connect(('racu.idea.sh', PortEnum.MAIN_SERVER.value))
    lastPin = self.server.db.executeQuery('select lastPIN from Config limit 1')
    print('lastPin =', lastPin)
    pinmsg = int.to_bytes(SocketEnum.PIN.value, 1, 'big') + int.to_bytes(lastPin[0]) if lastPin and 10**3<=lastPin[0]<10**4 else b''
    msg=''
    # while not msg:
    self.sendall(pinmsg)
    msg = self.recv()
    if not msg:
      print('main server connect error')
      return
    
    # self._IPC,self._ipcMode=Template(),False
  # def recv(self,buffersize=-1):
  #   if self._ipcMode:
  #     path=join(self._ipcPath,'sToCPipe')
  #     msg=self._IPC.open_r(path).read()
  #     self._IPC.open_w(path).write('')
  #     return msg
  #   super().recv(buffersize)
  # def connect(self,mph):
  #   if exists(self._ipcPath):
  #     self._ipcMode=True
  #     self.send = self._IPC.open_w(join(self._ipcPath,'cToSPipe')).write
  #   else:
  #     self._ipcMode=None  # any better idea??
  #     try:
  #       super().connect(('racu.idea.sh',39274))
  #     except: pass
  #     msgByte=super().recv(3)
  #     self._PIN=int.from_bytes(msgByte[1:])
  #   sleep(1)
  # def getStrategyHash(self,url,type):
  #   self.sendall(b''.join(map(int.to_bytes,(SocketEnum.SYNC_FETCH,8723),(1,2),('big',)*2)))
  #   c=self.recv(1)
  # def getStrategy(self,url,type):
  #   pass
  # def getCertKey(self):
  #   pass
  def _searchLocalArea(self):
    for loc in range(1,256):
      self._connect(('0.0.0.%d' % loc, PortEnum.MAIN_SERVER.value))
    pass