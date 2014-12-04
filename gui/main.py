# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Wed Dec  3 22:09:53 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(352, 90)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/client/RebAuth_res_32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.loginButton = QtWidgets.QPushButton(MainWindow)
        self.loginButton.setGeometry(QtCore.QRect(190, 10, 71, 21))
        self.loginButton.setObjectName("loginButton")
        self.changeButton = QtWidgets.QPushButton(MainWindow)
        self.changeButton.setEnabled(True)
        self.changeButton.setGeometry(QtCore.QRect(270, 10, 71, 21))
        self.changeButton.setObjectName("changeButton")
        self.lineEdit = EncryptedLineEdit(MainWindow)
        self.lineEdit.setGeometry(QtCore.QRect(10, 10, 171, 20))
        self.lineEdit.setInputMask("")
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit.setObjectName("lineEdit")
        self.label_post_time_edit = QtWidgets.QLabel(MainWindow)
        self.label_post_time_edit.setGeometry(QtCore.QRect(190, 42, 121, 16))
        self.label_post_time_edit.setObjectName("label_post_time_edit")
        self.label_pre_time_limit = QtWidgets.QLabel(MainWindow)
        self.label_pre_time_limit.setGeometry(QtCore.QRect(100, 42, 56, 16))
        self.label_pre_time_limit.setObjectName("label_pre_time_limit")
        self.timeLimitLineEdit = QtWidgets.QLineEdit(MainWindow)
        self.timeLimitLineEdit.setGeometry(QtCore.QRect(140, 40, 41, 20))
        self.timeLimitLineEdit.setObjectName("timeLimitLineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(MainWindow)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 70, 101, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(MainWindow)
        self.label.setGeometry(QtCore.QRect(50, 72, 21, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(MainWindow)
        self.label_2.setGeometry(QtCore.QRect(190, 72, 21, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(MainWindow)
        self.lineEdit_3.setGeometry(QtCore.QRect(220, 70, 113, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.retranslateUi(MainWindow)
        self.loginButton.clicked.connect(self.lineEdit.clear)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "마스터 로그인"))
        self.loginButton.setText(_translate("MainWindow", "로그인"))
        self.changeButton.setText(_translate("MainWindow", "변경"))
        self.label_post_time_edit.setText(_translate("MainWindow", "분 후 자동 로그아웃"))
        self.label_pre_time_limit.setText(_translate("MainWindow", "부재시"))
        self.label.setText(_translate("MainWindow", "PIN"))
        self.label_2.setText(_translate("MainWindow", "PW"))

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

