from aqt import mw, os

this_addon_name = os.path.dirname(__file__)


class _settings:
    def _ensure_dir(self, name):
        if not os.path.isdir(name):
            os.makedirs(name)
        return name

    @property
    def profile_folder(self):
        return self._ensure_dir(mw.pm.profileFolder())

    @property
    def addons_folder(self):
        return self._ensure_dir(mw.addonManager.addonsFolder())

    @property
    def media_folder(self):
        return self._ensure_dir(os.path.join(self.profile_folder, "collection.media"))

    @property
    def this_addon_folder(self):
        return self._ensure_dir(mw.addonManager.addonsFolder(this_addon_name))

    @property
    def user_files_folder(self):
        return self._ensure_dir(os.path.join(self.this_addon_folder, "user_files"))

    @property
    def imported_db_path(self):
        return os.path.join(self.profile_folder, "youdao2anki_imported_words.db")

    @property
    def deck_template_file(self):
        return os.path.join(self.this_addon_folder, "data\Template.apkg")

    @property
    def addon_config(self):
        return mw.addonManager.getConfig(__name__)

    @property
    def config_file(self):
        return os.path.join(self.this_addon_folder, "config.json")


settings = _settings()


class _addon_config:
    def __init__(self):
        self.config = settings.addon_config

    def SaveConfig(self):
        mw.addonManager.writeConfig(__name__, self.config)

    @property
    def QueryWordOnce(self):
        value = self.config['QueryWordOnce']
        return True if value else False

    @QueryWordOnce.setter
    def QueryWordOnce(self, value):
        self.config['QueryWordOnce'] = True if value else False

    @property
    def WordVoiceType(self):
        return str(self.config['WordVoiceType']).strip().lower()

    @WordVoiceType.setter
    def WordVoiceType(self, value):
        self.config['WordVoiceType'] = str(value).strip().lower()


addon_config = _addon_config()
