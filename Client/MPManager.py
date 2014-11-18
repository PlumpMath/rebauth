from Singleton import Singleton
from LocalDBConnector import LocalDBConnector
from Cryptor import Cryptor
# from Crypto import Random,Util
from Crypto.Util.number import getPrime
from zxcvbn import password_strength as strength
from PyQt5 import QtCore,QtWebKitWidgets
@Singleton
class MPManager():
  dummyMsg='rebauth will guard your personal web informations'
  def __init__(self):
    self._browsers=[]
  def evalConfidence(self,msg):
    ''' :return 0~4 : strength '''
    return strength(msg)['score'] if len(msg) else 0
  def login(self,hash):
    if type(hash) is str:hash=self.cryptor.hash(hash)
    DB=LocalDBConnector.Instance()
    qry=DB.executeQuery
    tmp=qry('select CNT, dummy from Config limit 1')
    counter,dummy=None,None
    if not len(tmp) or not tmp[0] or not tmp[0][0] or not tmp[0][1]:# there's no MP yet. set MP
      counter=getPrime(128)
      self.cryptor = Cryptor(hash,counter)
      dummy=self.cryptor.encrypt(self.dummyMsg)
      DB.executeQuery('insert into Config values(?,?)',(counter,dummy))
      DB.commit()
    else:
      counter,dummy = tmp[0]
      self.cryptor = Cryptor(hash,counter)
      if self.cryptor.decrypt(dummy) != self.dummyMsg: return False
    view=QtWebKitWidgets.QWebView()
    view.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    # view.setUrl(QtCore.QUrl('http://www.google.com'))
    view.setUrl('http://www.google.com')
    view.show()
    self._browsers.append(view)
    return True
  '''
  def __login(self,event):
    view=QtWebKitWidgets.QWebView()
    # page=QtWebKitWidgets.QWebPage()
    view.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    # view.setPage(page)
    view.setUrl(QtCore.QUrl('http://www.google.com'))
    view.show()
    self.__browsers.append(view)
    for b in self.__browsers:
      print(b)
    # QtWebKitWidgets.QGraphicsWebView()
    MainWindow.getInstance().goTray()
    return False
  '''