from Singleton import Singleton
from .LocalDBConnector import LocalDBConnector
from .Cryptor import Cryptor
from Crypto.Util.number import getPrime
from zxcvbn import password_strength as strength
from PyQt5 import QtCore,QtWebKitWidgets
from threading import Thread, Timer, local
from Enum import StrategyEnum
from .WebBrowser import WebBrowser
__all__=['MPManager']
@Singleton
class MPManager():
  dummyMsg='rebauth will guard your personal web informations'
  def __init__(self):
    self._browsers=[]
    self._MPH=''
    self._timer=None
    # from Client import MainWindow
    # self._main=mainWindow
  def evalConfidence(self,msg):
    ''' :return 0~4 : strength '''
    return strength(msg)['score'] if len(msg) else 0
  def login(self,hash):
    if type(hash) is str:hash=self.cryptor.hash(hash)
    DB=LocalDBConnector.Instance()
    config=DB.getConfig()
    # print(hash, DB.getConfig())
    if config:
      if Cryptor(hash,config['CNT']).decrypt(config['dummy']) != self.dummyMsg: return False
    else:
      config={'CNT':getPrime(128),'dummy':'','MPexpire':5}#make new counter
    cryptor = Cryptor(hash, config['CNT']) #recreate cryptor with old counter if MP else create cryptor with new counter
    config['dummy']=cryptor.encrypt(self.dummyMsg)
    DB.updateConfig(config)#convert config to bytes for db and generate new dummy by encrypting again
    DB.socket.connect()
    self._MPH = hash
    self.mainView = WebBrowser(self)
    self._browsers.append(self.mainView)
    self.updateTimer(config['MPexpire'])
    return True
  def updateTimer(self,expireRate=None):
    ''' update timer counter for resetting MP expire on inputs '''
    if expireRate is None: expireRate = LocalDBConnector.Instance().getConfig()['MPexpire']
    self._timerCnt = expireRate
    self.mainView.setWindowTitle('RebAuth - Web [%d min]' % expireRate)
    if self._timer is None or not self._timer.is_alive():
      self._timerTick(True)
  def _timerTick(self,init=False):
    '''  for each minute, expire MP or reset the 1 min timer '''
    if self.mainView is None : return
    if not init: self._timerCnt -= 1
    if self._timerCnt<=0:
      self._timer=None
      for browser in self._browsers:
        self.removeBrowser(browser)
      self._expireMP()
      return
    else:
      self.mainView.setWindowTitle('RebAuth - Web [%d min]' % self._timerCnt)
      if self._timer is not None and self._timer.is_alive(): self._timer.cancel()
      self._timer = Timer(60, self._timerTick, (False,))
      self._timer.start()
  def removeBrowser(self, browser):
    try:
      self._browsers.remove(browser)
    except: pass
    if len(self._browsers) == 0:
      self._expireMP() #expire MP on all available browsers closed
  def getMPH(self):
    return self._MPH
  def _expireMP(self):
    self._MPH=''
    self._browsers.clear()
    self.mainView = None
    if self._timer:
      if self._timer.is_alive(): self._timer.cancel()
    from PyQt5.QtWidgets import QApplication, QWidget
    from Client.MainWindow import MainWindow
    # for w in QApplication.topLevelWindows():
       # print(w.objectName())
    for w in QApplication.topLevelWidgets():
      #   print(w.objectName())
      if w.objectName() == 'MainWindow':
        w.show()
        break
# mpManager = MPManager()