# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/DownloadYoudao.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 145)
        Dialog.setMaximumSize(QtCore.QSize(300, 16777215))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.account = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.account.setFont(font)
        self.account.setObjectName("account")
        self.horizontalLayout.addWidget(self.account)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.password = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.password.setFont(font)
        self.password.setInputMask("")
        self.password.setMaxLength(32767)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.horizontalLayout_2.addWidget(self.password)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.download = QtWidgets.QPushButton(Dialog)
        self.download.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.download.setFont(font)
        self.download.setObjectName("download")
        self.verticalLayout.addWidget(self.download)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_("导入有道单词本"))
        self.label.setText(_("账号"))
        self.label_2.setText(_("密码"))
        self.download.setText(_("下载单词"))

