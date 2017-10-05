# import the main window object (mw) from aqt
import random
import warnings

from anki.hooks import addHook, wrap
from aqt import mw
from aqt.deckchooser import DeckChooser
from aqt.modelchooser import ModelChooser
from aqt.qt import *
from aqt.studydeck import StudyDeck

from .Helpers import Kindle
from .Helpers.ToAnkiTxt import GetWordsFromText
from .Helpers.Tools import GetDesktopPath
from .Helpers.Youdao import Youdao
from .Helpers.quick_note_and_deck_button import setup_buttons, model_buttons, change_model_to, deck_buttons, \
    change_deck_to
from .settings import addon_config
from .ui import ConfigDialog
from .ui.DownloadYoudao import DownloadYoudao
from .utils import addMenu, addMenuItem, addMenuSeparator, clean_up_user_files

warnings.simplefilter("ignore")


class Manager:
    def __init__(self):
        super(Manager, self).__init__()
        addHook('profileLoaded', self.onProfileLoaded)

        # download from youdao count
        self.youdao_downloaded = 0
        self.total_for_processing = 0

    def setupModelChooser(self):

        ModelChooser.setupModels = wrap(
            ModelChooser.setupModels,
            lambda mc: setup_buttons(mc, model_buttons, "note type", change_model_to),
            "after")
        ModelChooser.change_model_to = change_model_to
        DeckChooser.setupDecks = wrap(
            DeckChooser.setupDecks,
            lambda dc: setup_buttons(dc, deck_buttons, "deck", change_deck_to),
            "after")
        DeckChooser.change_deck_to = change_deck_to

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
        # self.setupModelChooser()

        clean_up_user_files()

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
        dlg = DownloadYoudao(self.import_deck_name, mw)
        dlg.exec_()

    def ImportText(self):

        txt_file = self.showTxtSelection("选择文件")
        if not txt_file:
            return
        words_data = GetWordsFromText(txt_file)

        source_tag, accepted = QInputDialog.getText(mw, "标签", "请输入【来源】标签:", QLineEdit.Normal,
                                                    addon_config.DefaultSourceTag)
        if accepted:
            if str(source_tag).strip():
                addon_config.DefaultSourceTag = source_tag
                addon_config.SaveConfig()

                youdao = Youdao(self.import_deck_name, source_tag)
                youdao.query_youdao_data(words_data,
                                         "TextImport_{}.txt".format(random.randint(0, 100)))

    def ImportKindleVocab(self):
        kindle = Kindle.Kindle()
        words_data = kindle.VocabData
        if not words_data:
            QMessageBox.information(mw, '从Kindle导入', "没有找到Kindle或者Kindle生词本没有新词.")
            return

        youdao = Youdao(self.import_deck_name, "Kindle")

        if QMessageBox.question(mw, "从Kindle导入", "总共{}个生词，确认导入吗?".format(
                words_data.__len__())) == QMessageBox.Yes:
            youdao.query_youdao_data({stem: usage for stem, usage in words_data},
                                     "KindleImport_{}.txt".format(random.randint(0, 100)))

    @property
    def import_deck_name(self):

        ret = StudyDeck(
            mw, accept=_("Choose"),
            title=_("Choose Deck"), help="addingnotes",
            cancel=False, parent=mw, geomKey="selectDeck")

        if not ret.Accepted:
            return
        return ret.name
