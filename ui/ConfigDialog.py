import sqlite3

from aqt import mw, QDialog, pyqtSlot, QMessageBox

from .forms.config import Ui_dlg_config
from ..settings import addon_config, settings


# writeConfig
class ConfigDialog(QDialog, Ui_dlg_config):
    def __init__(self):
        super(ConfigDialog, self).__init__(mw)
        self.setupUi(self)
        self.load_config()

    def load_config(self):
        voice_type = addon_config.WordVoiceType
        store_imported = addon_config.QueryWordOnce

        getattr(self, '{}_voice'.format(voice_type)).setChecked(True)
        self.query_word_once.setChecked(store_imported)

    def _set_config_value(self, config_name, value):
        setattr(addon_config, config_name, value)
        addon_config.SaveConfig()

    @pyqtSlot(bool)
    def on_collins_voice_clicked(self, checked):
        if checked:
            self._set_config_value('WordVoiceType', 'collins')

    @pyqtSlot(bool)
    def on_youdao_voice_clicked(self, checked):
        if checked:
            self._set_config_value('WordVoiceType', 'youdao')

    @pyqtSlot(int)
    def on_query_word_once_stateChanged(self, checked):
        self._set_config_value('QueryWordOnce', checked)

    @pyqtSlot()
    def on_reset_imported_clicked(self):
        con = sqlite3.connect(settings.imported_db_path)
        try:
            con.cursor().execute("DELETE FROM table_imported_words")
        except sqlite3.OperationalError:
            pass

        con.close()
        QMessageBox.information(mw, "重置", "已经清理.")
