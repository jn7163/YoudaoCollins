from PyQt5.QtWidgets import QDialog
from anki.importing import TextImporter
from aqt import mw, pyqtSlot, QListWidgetItem

from .forms.deck_chooser import Ui_Dialog


class DeckChooser(QDialog, Ui_Dialog):
    def __init__(self, file):
        super(DeckChooser, self).__init__(mw)
        self.setupUi(self)
        self.importer = TextImporter(mw.col, file)
        self.importer.delimiter = "\t"
        self.importer.importMode = 0
        self.importer.allowHTML = True
        self.setup_decks()
        self.exec_()

    @pyqtSlot("QListWidgetItem*")
    def on_decks_itemClicked(self, item):
        assert isinstance(item, QListWidgetItem)
        did = mw.col.decks.id(item.text())
        mw.col.conf['curDeck'] = did
        self.importer.model['did'] = did
        mw.col.models.save(self.importer.model)
        mw.col.decks.select(did)

    @pyqtSlot("QListWidgetItem*")
    def on_decks_itemDoubleClicked(self, item):
        self.on_decks_itemClicked(item)
        self.accept()

    def setup_decks(self):
        self.decks.addItems(sorted(mw.col.decks.allNames()))

    def accept(self):
        super(DeckChooser, self).accept()
