from Singleton import Singleton
from .LocalDBConnector import LocalDBConnector
from .Cryptor import Cryptor
from Crypto.Util.number import getPrime
from zxcvbn import password_strength as strength
from PyQt5 import QtCore,QtWebKitWidgets
from threading import Timer

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
    cryptor = Cryptor(hash,config['CNT']) #recreate cryptor with old counter if MP else create cryptor with new counter
    config['dummy']=cryptor.encrypt(self.dummyMsg)
    DB.updateConfig(config)#convert config to bytes for db and generate new dummy by encrypting again
    # print(hash, DB.getConfig())
    DB.socket.connect()
    view=QtWebKitWidgets.QWebView()
    view.setWindowTitle('RebAuth - Web')
    view.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    view.setUrl(QtCore.QUrl('http://www.google.com'))
    view.showMaximized()
    view.urlChanged=self.onUrlChange
    view.destroyed.connect(self._expireMP)
    self._browsers.append(view)
    self._MPH = hash
    if self._timer is None:
      self._timer = Timer(config['MPexpire']*60,self._expireMP)
    else:
      if self._timer.is_alive(): self._timer.cancel()
    self._timer.start()
    return True
  def getMPH(self):
    return self._MPH
  def _expireMP(self):
    self._MPH=''
    self._browsers.clear()
    from PyQt5.QtWidgets import QApplication, QWidget
    from Client.MainWindow import MainWindow
    # for w in QApplication.topLevelWindows():
    #   print(w.objectName())
    # print('------------')
    for w in QApplication.topLevelWidgets():
      #   print(w.objectName())
      if w.objectName() == 'MainWindow':
        w.show()
        print('main showed')
        break
  def onUrlChange(self,url):
    print(LocalDBConnector.Instance().executeQuery("select * from auth limit 1 where url=?",url))
# mpManager = MPManager()