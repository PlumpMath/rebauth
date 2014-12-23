# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Tue Nov 11 23:14:55 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebKitWidgets
from .LocalDBConnector import LocalDBConnector
from .MPManager import MPManager
__all__=['MainWindow']

class Ui_MainWindow(object):
  def setupUi(self, MainWindow):
    MainWindow.setObjectName('MainWindow')
    self.loginButton = QtWidgets.QPushButton(MainWindow)
    self.loginButton.setGeometry(QtCore.QRect(270, 10, 71, 21))
    self.loginButton.setObjectName('loginButton')
    self.changeButton = QtWidgets.QPushButton(MainWindow)
    self.changeButton.setEnabled(True)
    self.changeButton.setGeometry(QtCore.QRect(270, 10, 71, 21))
    self.changeButton.setObjectName('changeButton')
    self.noMP=noMP = not LocalDBConnector.Instance().getConfig()
    self.MPLineEdit = EncryptedLineEdit(MainWindow, noMP)
    self.MPLineEdit.setGeometry(QtCore.QRect(10, 10, 251, 20))
    self.MPLineEdit.setObjectName('MPLineEdit')
    self.MPLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
    if noMP: # add verifying line edit for initial set of MP
      self.MPCheckLineEdit = EncryptedLineEdit(MainWindow,noMP, verifier=self.MPLineEdit)
      self.MPCheckLineEdit.setGeometry(QtCore.QRect(10, 35, 251, 20))
      self.MPCheckLineEdit.setObjectName('MPCheckLineEdit')
      self.MPCheckLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
    # MP expire rate setting frame
    self.frame = QtWidgets.QFrame(MainWindow)
    self.frame.setGeometry(QtCore.QRect(0, 70, 351, 41))
    self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
    self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
    self.frame.setObjectName("frame")
    self.label = QtWidgets.QLabel(MainWindow)
    self.label.setGeometry(QtCore.QRect(50, 40, 21, 20))
    self.label.setObjectName("label")
    self.PINLineEdit = QtWidgets.QLineEdit(MainWindow)
    self.PINLineEdit.setGeometry(QtCore.QRect(80, 40, 101, 20))
    self.PINLineEdit.setObjectName("PINLineEdit")
    self.PINLineEdit.setEnabled(False)
    self.PWLineEdit = QtWidgets.QLineEdit(MainWindow)
    self.PWLineEdit.setGeometry(QtCore.QRect(210, 40, 113, 20))
    self.PWLineEdit.setObjectName("PWLineEdit")
    self.PWLineEdit.setEnabled(False)
    self.label_2 = QtWidgets.QLabel(MainWindow)
    self.label_2.setGeometry(QtCore.QRect(190, 40, 21, 20))
    self.label_2.setObjectName("label_2")
    self.label_pre_time_limit = QtWidgets.QLabel(self.frame)
    self.label_pre_time_limit.setGeometry(QtCore.QRect(100, 10, 56, 20))
    self.label_pre_time_limit.setObjectName("label_pre_time_limit")
    self.timeLimitLineEdit = QtWidgets.QLineEdit(self.frame)
    self.timeLimitLineEdit.setGeometry(QtCore.QRect(140, 10, 41, 20))
    self.timeLimitLineEdit.setObjectName("timeLimitLineEdit")
    self.label_post_time_edit = QtWidgets.QLabel(self.frame)
    self.label_post_time_edit.setGeometry(QtCore.QRect(190, 10, 121, 20))
    self.label_post_time_edit.setObjectName("label_post_time_edit")
    self.retranslateUi(MainWindow)
    QtCore.QMetaObject.connectSlotsByName(MainWindow)
    self.loginButton.clicked.connect(self.MPLineEdit.login)
    self.center(MainWindow)
    self.MPLineEdit.setFocus()
    # icon setting
    from Client import clientResources_rc
    self.icon=QtGui.QIcon()
    self.icon.addPixmap(QtGui.QPixmap(':/client/resources/RebAuth_res_32.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    MainWindow.setWindowIcon(self.icon)
    # tray icon and context menu
    if QtWidgets.QSystemTrayIcon.isSystemTrayAvailable():
      self.trayIcon=QtWidgets.QSystemTrayIcon(self.icon,MainWindow)
      self._traymenu=QtWidgets.QMenu('RebAuth <unlocked>',MainWindow)
      menus = list(map(QtWidgets.QAction,('종료(&c)', '로그아웃(&l)', '마스터 권한 설정(&m)', '개인정보설정(&s)'),(MainWindow,)*4))
      menus[0].setShortcut(QtGui.QKeySequence.Quit)
      for i, item in enumerate((MainWindow.close, MPManager.Instance()._expireMP, MainWindow.showMPsetting, MainWindow.PIsetting)):
        menus[i].triggered.connect(item)
      menus.reverse()
      self._traymenu.addActions(menus)
      self._traymenu.insertSeparator(menus[-1])
      # for item in (menus[0], 'sep', menus[1:]):
      #   if item == 'sep': self._traymenu.addSeparator()
      #   elif type(item) in (QtWidgets.QMenu, QtWidgets.QAction, QtWidgets.QWidgetAction): self._traymenu.addAction(item)
      self.trayIcon.setContextMenu(self._traymenu)
      self.trayIcon.activated.connect(self.onIconActivated)
    else:
      self.trayIcon, self._traymenu = None, None
    MainWindow.show()
  def retranslateUi(self, MainWindow):
    _translate = QtCore.QCoreApplication.translate
    MainWindow.setWindowTitle(_translate('MainWindow', '마스터 로그인'))
    self.loginButton.setText(_translate('MainWindow', 'MP생성' if self.noMP else '로그인'))
    self.changeButton.setText(_translate('MainWindow', 'MP변경'))
    self.label.setText(_translate("MainWindow", "PIN"))
    self.label_2.setText(_translate("MainWindow", "PW"))
    self.label_pre_time_limit.setText(_translate('MainWindow', '부재시'))
    self.label_post_time_edit.setText(_translate('MainWindow', '분 후 자동 로그아웃'))
  def onIconActivated(self, reason):
    self._traymenu.exec()
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
    from sys import argv, exit
    self.app = app = QtWidgets.QApplication(argv)
    self.PIsettingDialog=None
    self.settingMode = False
    super().__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    exit(app.exec_())
  def show(self):
    self.showLogin()
  def hide(self):
    if self.ui.trayIcon:
      self.ui.trayIcon.show()
    super().hide()
  def close(self):
    super().close()
    self.app.quit()
  def closeEvent(self, e):
    if self.settingMode:
      height = self.height() - self.ui.frame.height()
      for trg in self.setFixedHeight, self.setMaximumHeight, self.setMinimumHeight:
        trg(height)
      DB = LocalDBConnector.Instance()
      config = DB.getConfig()
      limit = self.ui.timeLimitLineEdit.text()
      if limit.isdigit() and 1 <= int(limit) <= 30:
        config['MPexpire'] = int(limit)
        DB.updateConfig(config)
        MPManager.Instance().updateTimer(config['MPexpire'])
      self.setWindowTitle(QtCore.QCoreApplication.translate('MainWindow', '마스터 로그인'))
      self.hide()
    else:
      self.app.quit()
  def showLogin(self):
    if self.ui.trayIcon: self.ui.trayIcon.hide()
    self.settingMode = False
    self.ui.MPLineEdit.setFocus()
    MPSettingFrameHeight = self.ui.frame.height()
    self.setMinimumSize(QtCore.QSize(352, 112 - MPSettingFrameHeight))
    self.setMaximumSize(QtCore.QSize(352, 112 - MPSettingFrameHeight))
    self.setFixedSize(352, 112 - MPSettingFrameHeight)
    self.ui.frame.hide()
    self.ui.loginButton.show()
    self.ui.changeButton.hide()
    super().show()
    try:
      self.PIsettingDialog.close()
    except: pass
  def showMPsetting(self):
    if self.isVisible(): return
    super().show()
    self.setWindowTitle(QtCore.QCoreApplication.translate('MainWindow', '마스터 권한 설정'))
    self.settingMode=True
    height = self.height() + self.ui.frame.height()
    for trg in self.setMaximumHeight, self.setMinimumHeight, self.setFixedHeight:
      trg(height)
    self.ui.timeLimitLineEdit.setText(str(LocalDBConnector.Instance().getConfig()['MPexpire']))
    self.ui.frame.show()
    self.ui.loginButton.hide()
    self.ui.changeButton.show()
  def PIsetting(self):
    if self.PIsettingDialog is None:
      self.PIsettingDialog = QtWidgets.QDialog()
      PIsettingUI = Ui_PISettingDialog()
      PIsettingUI.setupUi(self.PIsettingDialog)
      self.PIsettingDialog.show()
    else:
      self.PIsettingDialog.show()

class Ui_PISettingDialog(object):
  def setupUi(self, PISettingDialog):
    PISettingDialog.setObjectName('PISettingDialog')
    PISettingDialog.resize(320, 600)
    PISettingDialog.setMinimumSize(QtCore.QSize(320, 600))
    PISettingDialog.setSizeGripEnabled(False)
    # PISettingDialog.setModal(True)
    self.buttonBox = QtWidgets.QDialogButtonBox(PISettingDialog)
    self.buttonBox.setGeometry(QtCore.QRect(10, 570, 301, 32))
    self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
    self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
    self.buttonBox.setObjectName('buttonBox')
    self.bDayDateTimeEdit = QtWidgets.QDateTimeEdit(PISettingDialog)
    self.bDayDateTimeEdit.setGeometry(QtCore.QRect(120, 160, 190, 22))
    self.bDayDateTimeEdit.setObjectName('bDayDateTimeEdit')
    self.label = QtWidgets.QLabel(PISettingDialog)
    self.label.setGeometry(QtCore.QRect(10, 160, 70, 20))
    self.label.setObjectName('label')
    self.label_1 = QtWidgets.QLabel(PISettingDialog)
    self.label_1.setGeometry(QtCore.QRect(10, 70, 70, 20))
    self.label_1.setObjectName('label_1')
    self.lastNameLineEdit = QtWidgets.QLineEdit(PISettingDialog)
    self.lastNameLineEdit.setGeometry(QtCore.QRect(120, 70, 190, 20))
    self.lastNameLineEdit.setObjectName('lastNameLineEdit')
    self.label_2 = QtWidgets.QLabel(PISettingDialog)
    self.label_2.setGeometry(QtCore.QRect(10, 100, 70, 20))
    self.label_2.setObjectName('label_2')
    self.firstNameLineEdit = QtWidgets.QLineEdit(PISettingDialog)
    self.firstNameLineEdit.setGeometry(QtCore.QRect(120, 100, 190, 20))
    self.firstNameLineEdit.setObjectName('firstNameLineEdit')
    self.label_3 = QtWidgets.QLabel(PISettingDialog)
    self.label_3.setGeometry(QtCore.QRect(10, 40, 70, 20))
    self.label_3.setObjectName('label_3')
    self.line = QtWidgets.QFrame(PISettingDialog)
    self.line.setGeometry(QtCore.QRect(7, 240, 311, 16))
    self.line.setFrameShape(QtWidgets.QFrame.HLine)
    self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
    self.line.setObjectName('line')
    self.label_4 = QtWidgets.QLabel(PISettingDialog)
    self.label_4.setGeometry(QtCore.QRect(10, 130, 70, 20))
    self.label_4.setObjectName('label_4')
    self.middleNameLineEdit = QtWidgets.QLineEdit(PISettingDialog)
    self.middleNameLineEdit.setGeometry(QtCore.QRect(120, 130, 190, 20))
    self.middleNameLineEdit.setObjectName('middleNameLineEdit')
    self.maleRadioButton = QtWidgets.QRadioButton(PISettingDialog)
    self.maleRadioButton.setGeometry(QtCore.QRect(120, 40, 90, 20))
    self.maleRadioButton.setChecked(True)
    self.maleRadioButton.setObjectName('maleRadioButton')
    self.femaleRadioButton = QtWidgets.QRadioButton(PISettingDialog)
    self.femaleRadioButton.setGeometry(QtCore.QRect(220, 40, 90, 20))
    self.femaleRadioButton.setObjectName('femaleRadioButton')
    self.idLineEdit = QtWidgets.QLineEdit(PISettingDialog)
    self.idLineEdit.setGeometry(QtCore.QRect(120, 10, 190, 20))
    self.idLineEdit.setObjectName('idLineEdit')
    self.label_5 = QtWidgets.QLabel(PISettingDialog)
    self.label_5.setGeometry(QtCore.QRect(10, 10, 70, 20))
    self.label_5.setObjectName('label_5')
    self.label_6 = QtWidgets.QLabel(PISettingDialog)
    self.label_6.setGeometry(QtCore.QRect(10, 190, 70, 20))
    self.label_6.setObjectName('label_6')
    self.emailLineEdit = QtWidgets.QLineEdit(PISettingDialog)
    self.emailLineEdit.setGeometry(QtCore.QRect(120, 190, 190, 20))
    self.emailLineEdit.setObjectName('emailLineEdit')
    self.calendarWidget = QtWidgets.QCalendarWidget(PISettingDialog)
    self.calendarWidget.setEnabled(True)
    self.calendarWidget.setGeometry(QtCore.QRect(120, 180, 168, 155))
    self.calendarWidget.setObjectName('calendarWidget')
    self.calendarWidget.hide()
    self.mobilePhoneLineEdit = QtWidgets.QLineEdit(PISettingDialog)
    self.mobilePhoneLineEdit.setGeometry(QtCore.QRect(120, 220, 190, 20))
    self.mobilePhoneLineEdit.setObjectName('mobilePhoneLineEdit')
    self.label_7 = QtWidgets.QLabel(PISettingDialog)
    self.label_7.setGeometry(QtCore.QRect(10, 220, 70, 20))
    self.label_7.setObjectName('label_7')

    self.addrScrollArea = QtWidgets.QScrollArea(PISettingDialog)
    self.addrScrollArea.setGeometry(QtCore.QRect(0, 250, 321, 321))
    self.addrScrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
    self.addrScrollArea.setFrameShadow(QtWidgets.QFrame.Sunken)
    self.addrScrollArea.setLineWidth(1)
    self.addrScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
    self.addrScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    self.addrScrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
    self.addrScrollArea.setWidgetResizable(True)
    self.addrScrollArea.setObjectName('addrScrollArea')
    self.scrollAreaWidgetContents = QtWidgets.QWidget()
    self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, -361, 304, 682))
    self.scrollAreaWidgetContents.setObjectName('scrollAreaWidgetContents')
    self.formLayout = QtWidgets.QFormLayout(self.scrollAreaWidgetContents)
    self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
    self.formLayout.setObjectName('formLayout')

    self.labels=[QtWidgets.QLabel(self.scrollAreaWidgetContents) for i in range(15)]
    for i, label in enumerate(self.labels):
      label.setObjectName('label_' + str(8 + i))
      self.formLayout.setWidget(i, QtWidgets.QFormLayout.LabelRole, label)

    self.homeCountryLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
    self.homeCountryLineEdit.setObjectName('homeCountryLineEdit')
    self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.homeCountryLineEdit)
    self.homeCityLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
    self.homeCityLineEdit.setObjectName('homeCityLineEdit')
    self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.homeCityLineEdit)
    self.homeAddrTextEdit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
    self.homeAddrTextEdit.setObjectName('homeAddrTextEdit')
    self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.homeAddrTextEdit)
    self.homeDetailAddrTextEdit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
    self.homeDetailAddrTextEdit.setObjectName('homeDetailAddrTextEdit')
    self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.homeDetailAddrTextEdit)
    self.homeNumAddrTextEdit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
    self.homeNumAddrTextEdit.setObjectName('homeNumAddrTextEdit')
    self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.homeNumAddrTextEdit)
    self.homePostLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
    self.homePostLineEdit.setObjectName('homePostLineEdit')
    self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.homePostLineEdit)
    self.homePhoneLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
    self.homePhoneLineEdit.setObjectName('homePhoneLineEdit')
    self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.homePhoneLineEdit)
    self.companyNameLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
    self.companyNameLineEdit.setObjectName('companyNameLineEdit')
    self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.companyNameLineEdit)
    self.companyCountryLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
    self.companyCountryLineEdit.setObjectName('companyCountryLineEdit')
    self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.companyCountryLineEdit)
    self.companyCityLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
    self.companyCityLineEdit.setObjectName('companyCityLineEdit')
    self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.companyCityLineEdit)
    self.companyAddrTextEdit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
    self.companyAddrTextEdit.setObjectName('companyAddrTextEdit')
    self.formLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.companyAddrTextEdit)
    self.companyDetailAddrTextEdit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
    self.companyDetailAddrTextEdit.setObjectName('companyDetailAddrTextEdit')
    self.formLayout.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.companyDetailAddrTextEdit)
    self.companyNumAddrTextEdit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
    self.companyNumAddrTextEdit.setObjectName('companyNumAddrTextEdit')
    self.formLayout.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.companyNumAddrTextEdit)
    self.companyPostLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
    self.companyPostLineEdit.setObjectName('companyPostLineEdit')
    self.formLayout.setWidget(13, QtWidgets.QFormLayout.FieldRole, self.companyPostLineEdit)
    self.companyPhoneLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
    self.companyPhoneLineEdit.setObjectName('companyPhoneLineEdit')
    self.formLayout.setWidget(14, QtWidgets.QFormLayout.FieldRole, self.companyPhoneLineEdit)
    self.addrScrollArea.setWidget(self.scrollAreaWidgetContents)

    self.retranslateUi(PISettingDialog)
    self.buttonBox.accepted.connect(PISettingDialog.accept)
    self.buttonBox.rejected.connect(PISettingDialog.reject)
    QtCore.QMetaObject.connectSlotsByName(PISettingDialog)

    taborder = (self.idLineEdit, self.maleRadioButton, self.femaleRadioButton, self.lastNameLineEdit, self.firstNameLineEdit, self.middleNameLineEdit, self.bDayDateTimeEdit, self.emailLineEdit, self.calendarWidget, self.mobilePhoneLineEdit, self.addrScrollArea, self.homeCountryLineEdit, self.homeCityLineEdit, self.homeAddrTextEdit, self.homeDetailAddrTextEdit, self.homeNumAddrTextEdit, self.homePostLineEdit, self.homePhoneLineEdit, self.companyNameLineEdit, self.companyCountryLineEdit, self.companyCityLineEdit, self.companyAddrTextEdit, self.companyDetailAddrTextEdit, self.companyNumAddrTextEdit, self.companyPhoneLineEdit)
    for i in range(len(taborder)-1):
      PISettingDialog.setTabOrder(taborder[i],taborder[i+1])

  def retranslateUi(self, PISettingDialog):
    _translate = QtCore.QCoreApplication.translate
    PISettingDialog.setWindowTitle(_translate('PISettingDialog', '개인정보 설정'))
    self.label.setText(_translate('PISettingDialog', '생일'))
    self.label_1.setText(_translate('PISettingDialog', '성'))
    self.label_2.setText(_translate('PISettingDialog', '이름'))
    self.label_3.setText(_translate('PISettingDialog', '성별'))
    self.label_4.setText(_translate('PISettingDialog', '중간이름'))
    self.maleRadioButton.setText(_translate('PISettingDialog', '남자'))
    self.femaleRadioButton.setText(_translate('PISettingDialog', '여자'))
    self.label_5.setText(_translate('PISettingDialog', '기본ID'))
    self.label_6.setText(_translate('PISettingDialog', '이메일'))
    self.label_7.setText(_translate('PISettingDialog', '휴대전화번호'))
    labelNames=['국가','도시','주소','세부주소','지번 및 건물번호','우편번호','전화번호']
    labelNames=['주거지 ' + name for name in labelNames]+['근무지 ' + name for name in ['이름']+labelNames]
    for name in labelNames:
      '주거지 ' + name
    for i, label in enumerate(self.labels):
      label.setText(_translate('PISettingDialog', labelNames[i]))