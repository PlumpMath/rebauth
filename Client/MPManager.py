from Singleton import Singleton
from LocalDBConnector import LocalDBConnector
from Cryptor import Cryptor
# from Crypto import Random,Util
from Crypto.Util.number import getPrime
from zxcvbn import password_strength as strength
from PyQt5 import QtCore,QtWebKitWidgets
@Singleton
class MPManager():
  def __init__(self):
    self._browsers=[]
  def evalConfidence(self,msg):
    ''' :return 0~4 : strength '''
    return strength(msg)
  def login(self,hash):
    if type(hash) is str:hash=self.cryptor.hash(hash)
    qry=LocalDBConnector.instance().executeQuery
    tmp=qry('select CNT, dummy from Config limit 1')
    DB=LocalDBConnector.Instance()
    DB.executeQuery('insert into Config values(?,?)',())
    DB.commit()
  if MPManager.Instance().login():self.parent().goTray()
    if not len(tmp) or not tmp[0] or not tmp[1]:
      pass
    if not len(counter):
      new_counter=getPrime(128)
      qry('replace into config_val_key where id=?',counter)
      counter=new_counter
    self.cryptor = Cryptor(hash,counter)
    if not len(dummy):
      counter,dummy=list(map(lambda type,arg:qry('select value from config_val_%s where id=?'%type,arg),('int','key'),list(map(int,(counter,dummy)))))
    self.cryptor = Cryptor(hash,counter)
    view=QtWebKitWidgets.QWebView()
    view.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    view.setUrl(QtCore.QUrl('http://www.google.com'))
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