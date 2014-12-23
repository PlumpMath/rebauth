from string import ascii_letters,punctuation,digits
from Crypto import Cipher
from Crypto.Cipher import AES
from Crypto.Random import random
from PyQt5 import QtCore, QtGui, QtWidgets
from Client.MPManager import MPManager
from Client.Cryptor import hash

__all__=['EncryptedLineEdit']

class EncryptedLineEdit(QtWidgets.QLineEdit):
  def __init__(self,MainWindow,noMP,verifier=None):
    super().__init__(MainWindow)
    self.setAttribute(QtCore.Qt.WA_InputMethodEnabled)
    self.availChars=digits+ascii_letters+punctuation
    self.getRandChar=lambda : random.choice(self.availChars)
    self._realString=''
    self._noMP=noMP
    self._verifier=verifier
  def keyPressEvent(self,event): #QKeyEvent
    key=event.key()
    char=event.text() if event.text() in self.availChars else '' #else chr(key)if (key in range(0xffff) and chr(key) in self.availChars)
    #print(event.text(),event.text() in self.availChars,char)
    backspaceKey,deleteKey=QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Delete
    if key in [backspaceKey,deleteKey] or char:
      pos,width=self.cursorPosition(),len(self.selectedText())
      self._realString=self._realString[:pos-(1 if key==backspaceKey else 0)]+char+self._realString[pos-(1 if key==deleteKey else 0)+width:]
      if char:
        randChar=self.getRandChar()
        print(randChar)
        event=QtGui.QKeyEvent(QtCore.QEvent(QtCore.QEvent.KeyPress).type(),ord(randChar),event.modifiers(),randChar)
      if self._verifier:
        QtWidgets.QToolTip.showText(self.mapToGlobal(QtCore.QPoint()),'일치합니다.' if self._verifier.equals(hash(self._realString)) else '일치하지 않습니다.')
      else:
        QtWidgets.QToolTip.showText(self.mapToGlobal(QtCore.QPoint()), ('너무 위험합니다.','더 복잡해야 합니다.','조금 더 복잡해야 합니다.','안전합니다.','매우 안전합니다.')[MPManager.Instance().evalConfidence(self._realString)]) #str(MPManager.Instance().evalConfidence(self._realString)))
    elif key in [QtCore.Qt.Key_Return,QtCore.Qt.Key_Enter]:
      self.login()
    super().keyPressEvent(event)
  def login(self,event=None):
    if MPManager.Instance().evalConfidence(self._realString)<4 :
      QtWidgets.QMessageBox.critical(self, '로그인 에러', '마스터 패스워드가 틀렸습니다.')
      return False
    MPH=hash(self._realString)
    print(self.text())
    print(MPH)
    if self._noMP:
      theOtherEdit=self._verifier if self._verifier else self.parent().findChild(type(self),'MPCheckLineEdit')
      if not theOtherEdit.equals(MPH):return False
    if MPManager.Instance().login(MPH): #login success
      self.clear()
      if self._noMP:
        self._noMP=False
        self.parent().findChild(type(self),'MPCheckLineEdit').close()
      # loginButt,changeButt=list(map(self.parent().findChild,(QtWidgets.QPushButton,)*2,('loginButton','changeButton')))
      # if loginButt: loginButt.hide()
      # if changeButt: changeButt.show()
      self.parent().hide()
      self.parent().ui.trayIcon.showMessage('MP 로그인','마스터로 로그인 되었습니다.')
    return False
  def clear(self):
    super().clear()
    self._realString = ''
  def equals(self,hashToCompare):
    return hash(self._realString)==hashToCompare