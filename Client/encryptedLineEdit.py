from string import ascii_letters,punctuation,digits
from Crypto import Cipher
from Crypto.Cipher import AES
from Crypto.Random import random
from PyQt5 import QtCore, QtGui, QtWidgets
from MPManager import MPManager
from Cryptor import Cryptor

hash=Cryptor.hash

class EncryptedLineEdit(QtWidgets.QLineEdit):
  def __init__(self,MainWindow,noMP,verifier=None):
    super().__init__(MainWindow)
    self.setAttribute(QtCore.Qt.WA_InputMethodEnabled)
    self.availChars=digits+ascii_letters+punctuation
    self.getRandChar=lambda : random.choice(self.availChars)
    self._realString=''
    if noMP and not verifier: #no mp set. make another verifying input
      MainWindow.MPCheckLineEdit = EncryptedLineEdit(MainWindow,noMP, verifier=self)
      w,h=self.width(),self.height()
      MainWindow.MPCheckLineEdit.setGeometry(self.rect().adjusted(0,h+5,w,h+5))
      MainWindow.MPCheckLineEdit.setObjectName("MPCheckLineEdit")
      MainWindow.MPCheckLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
    self._noMP=noMP
    self._verifier=verifier
  def keyPressEvent(self,event): #QKeyEvent
    key=event.key()
    char=event.text() if event.text() in self.availChars else '' #else chr(key)if (key in range(0xffff) and chr(key) in self.availChars)
    #print(event.text(),event.text() in self.availChars,char)
    backspaceKey,deleteKey=QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Delete
    if key in [backspaceKey,deleteKey] or char:
      pos=self.cursorPosition()
      self._realString=self._realString[:pos-(1 if key==backspaceKey else 0)]+char+self._realString[pos-(1 if key==deleteKey else 0):]
      if char:
        randChar=self.getRandChar()
        event=QtGui.QKeyEvent(QtCore.QEvent(QtCore.QEvent.KeyPress).type(),ord(randChar),event.modifiers(),randChar)
      if self._verifier:
        QtWidgets.QToolTip.showText(self.mapToGlobal(QtCore.QPoint()),'일치합니다.' if self._verifier.equals(hash(self._realString)) else '일치하지 않습니다.')
      else:
        QtWidgets.QToolTip.showText(self.mapToGlobal(QtCore.QPoint()), ('너무 위험합니다.','더 복잡해야 합니다.','조금 더 복잡해야 합니다.','안전합니다.','매우 안전합니다.')[MPManager.Instance().evalConfidence(self._realString)]) #str(MPManager.Instance().evalConfidence(self._realString)))
    elif key in [QtCore.Qt.Key_Return,QtCore.Qt.Key_Enter]:
      self.login()
    super().keyPressEvent(event)
  def login(self,event=None):
    if MPManager.Instance().evalConfidence(self._realString)<4 : return False
    MPH=hash(self._realString)
    if self._noMP:
      theOtherEdit=self._verifier if self._verifier else self.parent().MPCheckLineEdit
      if not theOtherEdit.equals(MPH):return False
    if MPManager.Instance().login(MPH): #login success
      if self._noMP:
        self._noMP=False
        self.parent().MPCheckLineEdit.close()
      self.parent().goTray()
    return False
  def equals(self,hashToCompare):
    return hash(self._realString)==hashToCompare