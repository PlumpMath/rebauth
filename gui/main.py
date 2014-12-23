# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Mon Dec 22 19:44:04 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(352, 112)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/client/RebAuth_res_32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.loginButton = QtWidgets.QPushButton(MainWindow)
        self.loginButton.setGeometry(QtCore.QRect(270, 10, 71, 21))
        self.loginButton.setObjectName("loginButton")
        self.changeButton = QtWidgets.QPushButton(MainWindow)
        self.changeButton.setEnabled(True)
        self.changeButton.setGeometry(QtCore.QRect(270, 10, 71, 21))
        self.changeButton.setObjectName("changeButton")
        self.lineEdit = EncryptedLineEdit(MainWindow)
        self.lineEdit.setGeometry(QtCore.QRect(10, 10, 251, 20))
        self.lineEdit.setInputMask("")
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit.setObjectName("lineEdit")
        self.frame = QtWidgets.QFrame(MainWindow)
        self.frame.setGeometry(QtCore.QRect(0, 70, 351, 41))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_pre_time_limit = QtWidgets.QLabel(self.frame)
        self.label_pre_time_limit.setGeometry(QtCore.QRect(100, 10, 56, 20))
        self.label_pre_time_limit.setObjectName("label_pre_time_limit")
        self.label_post_time_edit = QtWidgets.QLabel(self.frame)
        self.label_post_time_edit.setGeometry(QtCore.QRect(190, 10, 121, 20))
        self.label_post_time_edit.setObjectName("label_post_time_edit")
        self.timeLimitLineEdit = QtWidgets.QLineEdit(self.frame)
        self.timeLimitLineEdit.setGeometry(QtCore.QRect(140, 10, 41, 20))
        self.timeLimitLineEdit.setObjectName("timeLimitLineEdit")
        self.PWLineEdit = QtWidgets.QLineEdit(MainWindow)
        self.PWLineEdit.setEnabled(False)
        self.PWLineEdit.setGeometry(QtCore.QRect(210, 40, 113, 20))
        self.PWLineEdit.setObjectName("PWLineEdit")
        self.label_2 = QtWidgets.QLabel(MainWindow)
        self.label_2.setGeometry(QtCore.QRect(190, 40, 21, 20))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(MainWindow)
        self.label.setGeometry(QtCore.QRect(50, 40, 21, 20))
        self.label.setObjectName("label")
        self.PINLineEdit = QtWidgets.QLineEdit(MainWindow)
        self.PINLineEdit.setEnabled(False)
        self.PINLineEdit.setGeometry(QtCore.QRect(80, 40, 101, 20))
        self.PINLineEdit.setObjectName("PINLineEdit")

        self.retranslateUi(MainWindow)
        self.loginButton.clicked.connect(self.lineEdit.clear)
        MainWindow.destroyed.connect(self.label_2.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "마스터 로그인"))
        self.loginButton.setText(_translate("MainWindow", "로그인"))
        self.changeButton.setText(_translate("MainWindow", "변경"))
        self.label_pre_time_limit.setText(_translate("MainWindow", "부재시"))
        self.label_post_time_edit.setText(_translate("MainWindow", "분 후 자동 로그아웃"))
        self.label_2.setText(_translate("MainWindow", "PW"))
        self.label.setText(_translate("MainWindow", "PIN"))

from encryptedlineedit import EncryptedLineEdit
import clientResources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

