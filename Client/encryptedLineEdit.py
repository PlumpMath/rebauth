from string import ascii_letters,punctuation
from Crypto import Cipher
from Crypto.Cipher import AES
from Crypto.Random import random
from PyQt5 import QtCore, QtGui, QtWidgets
from MPManager import MPManager
from Cryptor.Cryptor import hash

class EncryptedLineEdit(QtWidgets.QLineEdit):
  def __init__(self,MainWindow,noMP,_isVerifier=False):
    super().__init__(MainWindow)
    self.setAttribute(QtCore.Qt.WA_InputMethodEnabled)
    self.availChars=ascii_letters+punctuation
    self.getRandChar=lambda : random.choice(self.availChars)
    self._realString=''
    if noMP : #no mp set. make another verifying input
      MainWindow.MPCheckLineEdit = EncryptedLineEdit(MainWindow,noMP,isVerifier=True)
      MainWindow.MPLineEdit.setGeometry(self.rect().adjusted(0,25,1,1))
      MainWindow.MPLineEdit.setObjectName("MPCheckLineEdit")
      MainWindow.MPLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
    self._noMP=noMP
    self._isVerifier=_isVerifier
  def keyPressEvent(self,event): #QKeyEvent
    key=event.key()
    char=chr(key) if (key in range(0xffff) and chr(key) in self.availChars) else ''
    print(char)
    backspaceKey,deleteKey=QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Delete
    if key in [backspaceKey,deleteKey] or char:
      pos=self.cursorPosition()
      self._realString=self._realString[:pos-(1 if key==backspaceKey else 0)]+char+self._realString[pos-(1 if key==deleteKey else 0):]
      if char:
        randChar=self.getRandChar()
        event=QtGui.QKeyEvent(QtCore.QEvent(QtCore.QEvent.KeyPress).type(),ord(randChar),event.modifiers(),randChar)
        QtWidgets.QToolTip.showText(self.mapToGlobal(QtCore.QPoint()), MPManager.Instance().evalConfidence(self._realString))#('너무 위험합니다.','더 복잡해야 합니다.','조금 더 복잡해야 합니다.','안전합니다.')[MPManager.Instance().evalConfidence(self._realString)])
    elif key in [QtCore.Qt.Key_Return,QtCore.Qt.Key_Enter]:
      print(self._realString)
      self.login()
    super().keyPressEvent(event)
  def login(self,event=None):
    MPH=hash(self.__realString)
    if self._noMP:
      theOtherEdit=self.parent().MPLineEdit if self._isVerifier else self.parent().MPCheckLineEdit
      if not theOtherEdit.equals(MPH):
        return False
    if MPManager.Instance().login(MPH): #login success
      if self._noMP:
        self._noMP=False
        self.parent().MPCheckLineEdit.close()
  def equals(self,hashToCompare):
    return hash(self.__realString)==hashToCompare