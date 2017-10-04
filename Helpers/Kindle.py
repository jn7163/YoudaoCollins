import sqlite3
import win32api

import os


class Kindle():
    def __init__(self):
        super(Kindle, self).__init__()

    @property
    def KindleDrive(self):
        for dr in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']:
            kindle_drive = "{}:\\".format(dr)
            try:
                dr_nm = win32api.GetVolumeInformation(kindle_drive)[0]
            except:
                continue
            kindle_version_txt = r"{}:\system\version.txt".format(dr)

            if dr_nm.upper() == "KINDLE" and os.path.isfile(kindle_version_txt):
                with open(kindle_version_txt) as f:
                    if f.readlines()[0].startswith("Kindle"):
                        return kindle_drive

    @property
    def VocabDBPath(self):
        kindle_drive = self.KindleDrive
        if kindle_drive:
            return os.path.join(kindle_drive, r"system\vocabulary\vocab.db")

    @property
    def VocabData(self):
        db = self.VocabDBPath
        if not db:
            return ()
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute( """
            SELECT
              words.stem,
              LOOKUPS.usage
            FROM words
              LEFT JOIN LOOKUPS ON words.id = LOOKUPS.word_key
            WHERE lang = 'en'
            """)
        self.words = c.fetchall()
        return self.words
