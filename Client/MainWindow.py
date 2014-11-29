# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Tue Nov 11 23:14:55 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebKitWidgets
from .LocalDBConnector import LocalDBConnector

__all__=['MainWindow']

class Ui_MainWindow(object):
  def setupUi(self, MainWindow):
    MainWindow.setObjectName("MainWindow")
    MainWindow.resize(352, 70)
    MainWindow.setMinimumSize(QtCore.QSize(352, 70))
    MainWindow.setMaximumSize(QtCore.QSize(352, 70))
    self.loginButton = QtWidgets.QPushButton(MainWindow)
    self.loginButton.setGeometry(QtCore.QRect(190, 10, 71, 21))
    self.loginButton.setObjectName("loginButton")
    self.changeButton = QtWidgets.QPushButton(MainWindow)
    self.changeButton.setEnabled(True)
    self.changeButton.setGeometry(QtCore.QRect(270, 10, 71, 21))
    self.changeButton.setObjectName("changeButton")
    self.changeButton.hide()
    self.noMP=noMP = not LocalDBConnector.Instance().getConfig()
    self.MPLineEdit = EncryptedLineEdit(MainWindow, noMP)
    self.MPLineEdit.setGeometry(QtCore.QRect(10, 10, 171, 20))
    self.MPLineEdit.setObjectName("MPLineEdit")
    self.MPLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
    if noMP: # add verifying line edit for initial set of MP
      self.MPCheckLineEdit = EncryptedLineEdit(MainWindow,noMP, verifier=self.MPLineEdit)
      self.MPCheckLineEdit.setGeometry(QtCore.QRect(10, 35, 171, 20))
      self.MPCheckLineEdit.setObjectName("MPCheckLineEdit")
      self.MPCheckLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
      self.loginButton.hitButton = self.MPLineEdit.login
    # self.label_post_time_edit = QtWidgets.QLabel(MainWindow)
    # self.label_post_time_edit.setGeometry(QtCore.QRect(190, 40, 121, 16))
    # self.label_post_time_edit.setObjectName("label_post_time_edit")
    # self.label_pre_time_limit = QtWidgets.QLabel(MainWindow)
    # self.label_pre_time_limit.setGeometry(QtCore.QRect(100, 40, 56, 16))
    # self.label_pre_time_limit.setObjectName("label_pre_time_limit")
    # self.timeLimitLineEdit = QtWidgets.QLineEdit(MainWindow)
    # self.timeLimitLineEdit.setGeometry(QtCore.QRect(140, 40, 41, 20))
    # self.timeLimitLineEdit.setObjectName("timeLimitLineEdit")

    self.retranslateUi(MainWindow)
    QtCore.QMetaObject.connectSlotsByName(MainWindow)
    self.center(MainWindow)
    self.MPLineEdit.setFocus()
    # self.lineEdit.focusWidget()

  def retranslateUi(self, MainWindow):
    _translate = QtCore.QCoreApplication.translate
    MainWindow.setWindowTitle(_translate("MainWindow", "마스터 로그인"))
    self.loginButton.setText(_translate("MainWindow", "MP생성" if self.noMP else "로그인"))
    self.changeButton.setText(_translate("MainWindow", "변경"))
    # self.label_post_time_edit.setText(_translate("MainWindow", "분 후 자동 로그아웃"))
    # self.label_pre_time_limit.setText(_translate("MainWindow", "부재시"))

  def center(self,MainWindow):
    qr = MainWindow.frameGeometry()
    cp = QtWidgets.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    MainWindow.move(qr.topLeft())
from .encryptedLineEdit import EncryptedLineEdit
from Singleton import Singleton
@Singleton
class MainWindow(QtWidgets.QWidget):
  def __init__(self):
    print('main init')
    from sys import argv, exit
    app = QtWidgets.QApplication(argv)
    super().__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self._trayIcon=QtWidgets.QSystemTrayIcon(self)
    self._traymenu=QtWidgets.QMenu(self)
    # self._traymenu.addAction()
    self._trayIcon.setContextMenu(self._traymenu)
    self.show()
    exit(app.exec_())
  def show(self):
    self._trayIcon.hide()
    super().show()
  def goTray(self):
    self._trayIcon.show()
    super().hide()
# mainWindow=None #MainWindow()