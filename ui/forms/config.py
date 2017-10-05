# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/config.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_dlg_config(object):
    def setupUi(self, dlg_config):
        dlg_config.setObjectName("dlg_config")
        dlg_config.resize(231, 137)
        self.gridLayout_2 = QtWidgets.QGridLayout(dlg_config)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(dlg_config)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.collins_voice = QtWidgets.QRadioButton(self.groupBox)
        self.collins_voice.setObjectName("collins_voice")
        self.horizontalLayout.addWidget(self.collins_voice)
        self.youdao_voice = QtWidgets.QRadioButton(self.groupBox)
        self.youdao_voice.setObjectName("youdao_voice")
        self.horizontalLayout.addWidget(self.youdao_voice)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(dlg_config)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.query_word_once = QtWidgets.QCheckBox(self.groupBox_2)
        self.query_word_once.setObjectName("query_word_once")
        self.horizontalLayout_2.addWidget(self.query_word_once)
        self.reset_imported = QtWidgets.QPushButton(self.groupBox_2)
        self.reset_imported.setObjectName("reset_imported")
        self.horizontalLayout_2.addWidget(self.reset_imported)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_2, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)

        self.retranslateUi(dlg_config)
        QtCore.QMetaObject.connectSlotsByName(dlg_config)

    def retranslateUi(self, dlg_config):
        _translate = QtCore.QCoreApplication.translate
        dlg_config.setWindowTitle(_("Configuration"))
        self.groupBox.setTitle(_("优先使用单词语音类型"))
        self.collins_voice.setToolTip(_("https://www.collinsdictionary.com"))
        self.collins_voice.setText(_("柯林斯"))
        self.youdao_voice.setText(_("有道"))
        self.groupBox_2.setTitle(_("其他"))
        self.query_word_once.setText(_("不重复查询"))
        self.reset_imported.setText(_("重置查询记录"))
