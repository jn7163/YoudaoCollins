import random

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .forms.DownloadYoudao import Ui_Dialog
from ..Helpers import Youdao


class DownloadYoudao(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(DownloadYoudao, self).__init__(parent)
        self.setupUi(self)
        self.read_account_info()
        self.parent = parent

        self.downloaded = 0
        self.total = 0

    def read_account_info(self):
        # load youdao id and passwords
        self.acct, self.pwd = Youdao.Youdao.GetAuth()

        if self.acct and self.pwd:
            self.account.setText(self.acct)
            self.password.setText(self.pwd)

    @pyqtSlot(bool)
    def on_download_clicked(self):
        Youdao.Youdao.SaveLocalAccount(self.account.text(), self.password.text())
        self.read_account_info()
        self.ConvertYoudaoWordList()

    def ConvertYoudaoWordList(self):
        self.hide()
        youdao = Youdao.Youdao("有道单词本")
        youdao.login(self.acct, self.pwd)
        words = youdao.GetWordList()
        youdao.query_youdao_data(words, "YoudaoWordlist_{}.txt".format(random.randint(0, 100)))
