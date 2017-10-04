# import the main window object (mw) from aqt
import warnings

from anki.hooks import addHook
from aqt import mw
from aqt.qt import *
from .ui import ConfigDialog

from .Helpers import Kindle
from .Helpers.ToAnkiTxt import GetWordsFromText
from .Helpers.Tools import GetDesktopPath
from .Helpers.Youdao import Youdao
from .ui.DownloadYoudao import DownloadYoudao
from .utils import addMenu, addMenuItem, addMenuSeparator

warnings.simplefilter("ignore")


class Manager:
    def __init__(self):
        super(Manager, self).__init__()
        addHook('profileLoaded', self.onProfileLoaded)

        # download from youdao count
        self.youdao_downloaded = 0
        self.total_for_processing = 0

    def setupAdditionalMenu(self):
        menu_name = "有道柯林斯"
        addMenu(menu_name)
        addMenuItem(menu_name, '从文本导入', self.ImportText, "ALT+1")
        addMenuSeparator(menu_name)
        addMenuItem(menu_name, '从有道单词本导入', self.ImportYoudaoWordlist, "ALT+2")
        addMenuItem(menu_name, '从Kindle生词导入', self.ImportKindleVocab, "ALT+3")
        addMenuSeparator(menu_name)
        addMenuItem(menu_name, '设置', self.ShowConfigDialog, )

    def onProfileLoaded(self):
        self.setupAdditionalMenu()

        # import dec template
        pass

    def ShowConfigDialog(self):
        dlg = ConfigDialog.ConfigDialog()
        dlg.exec_()

    def showTxtSelection(self, window_lable):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename = QFileDialog.getOpenFileName(mw,
                                               window_lable,
                                               GetDesktopPath(),
                                               filter="All Files(*);;Text Files (*.txt)",
                                               options=options)
        return filename[0]

    def ImportYoudaoWordlist(self):
        dlg = DownloadYoudao(mw)
        dlg.exec_()

    def ImportText(self):
        txt_file = self.showTxtSelection("选择文件")
        if not txt_file:
            return
        words_data = GetWordsFromText(txt_file)

        youdao = Youdao("Others")
        youdao.query_youdao_data(words_data, "TextImport.txt")

    def ImportKindleVocab(self):
        kindle = Kindle.Kindle()
        words_data = kindle.VocabData
        if not words_data:
            QMessageBox.information(mw, '从Kindle导入', "没有找到Kindle或者Kindle生词本没有新词.")
            return

        youdao = Youdao("Kindle")

        if QMessageBox.question(mw, "从Kindle导入", "总共{}个生词，确认导入吗?".format(
                words_data.__len__())) == QMessageBox.Yes:
            youdao.query_youdao_data({stem: usage for stem, usage in words_data}, "KindleImport.txt")
