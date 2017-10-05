import os
import re
import sqlite3

import bs4
import requests
from aqt import mw, QEventLoop, QMessageBox
from aqt.importing import importFile

from .ToAnkiTxt import TransToAnkiText
from ._WordlistSession import _WordListRequester
from ..Helpers.Importer import ImportToAnki
from ..settings import settings, addon_config


class Youdao(_WordListRequester):
    def __init__(self, import_deck_name='', source_tag=""):
        super(Youdao, self).__init__()
        self.translator = TransToAnkiText()
        self.source_tag = source_tag
        self.import_deck_name = import_deck_name

        self.youdao_downloaded = 0
        self.total_for_processing = 0

        # db con
        self.db_con = self.connect_db()
        self.db_cur = self.db_con.cursor()

        self.check_first_time_run()

    def check_first_time_run(self):
        is_first_time_run = mw.pm.profile.get('FirstTimeRunWord', True)
        if is_first_time_run:
            importFile(mw, settings.deck_template_file)
            mw.pm.profile['FirstTimeRunWord'] = False

    def connect_db(self):
        con = sqlite3.connect(settings.imported_db_path)
        try:
            con.cursor().execute('''CREATE TABLE imported_words (word TEXT)''')
        except sqlite3.OperationalError:
            pass

        return con

    @property
    def _ImportedWords(self):
        words = self.db_cur.execute("SELECT DISTINCT word FROM imported_words")
        if words:
            words = [i[0].upper() for i in words]
        return words

    def MarkWordImported(self, word):
        sql = "insert into imported_words (word) values(?)"
        self.db_cur.execute(sql, (word.upper().strip(),))
        self.db_con.commit()

    def ImportToAnki(self, file):
        mw.progress.finish()
        if os.path.isfile(file):
            ImportToAnki("有道柯林斯", self.import_deck_name, file=file)
        else:
            QMessageBox.information(mw, "导入", "没有新的生词导入")
        self.youdao_downloaded = 0
        self.total_for_processing = 0

    def CompleteOne(self):
        mw.progress.update(label="Getting data from Youdao.com ... {} / {}".format(self.youdao_downloaded,
                                                                                   self.total_for_processing))
        self.youdao_downloaded += 1

    def query_youdao_data(self, words_data, output_txt, ):

        mw.progress.start(immediate=True)
        mw.app.processEvents(QEventLoop.ExcludeUserInputEvents)
        self.translator.Complete.connect(self.ImportToAnki)
        self.translator.CompletedOne.connect(self.CompleteOne)

        self.total_for_processing = words_data.__len__()

        self.translator.trans_to_anki_text(
            words_data,
            os.path.join(settings.user_files_folder, output_txt),
            mp3_dir=settings.media_folder,
            source_tag=self.source_tag
        )

    @staticmethod
    def SaveLocalAccount(id, pwd):
        mw.pm.profile["youdao_account"] = id
        mw.pm.profile["youdao_pwd"] = pwd

    @staticmethod
    def GetAuth():
        return mw.pm.profile.get("youdao_account"), mw.pm.profile.get("youdao_pwd")

    def get_word_dict(self, word, sound_dir="DownloadedSounds"):

        expl_dict = dict()

        if addon_config.QueryWordOnce:
            if word.upper() in self._ImportedWords:
                raise Exception("Imported word: {}".format(word))

        my_headers = {
            'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, image/webp, */*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN, zh;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'Host': 'dict.youdao.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                           Chrome/48.0.2564.116 Safari/537.36'
        }
        url = 'http://dict.youdao.com/search?q={}'.format(word)
        res = requests.get(url, headers=my_headers)

        if "dog.yodao.com" in res.url:
            print("Please verify at {}\n".format(res.url))
            input("Enter to continue ...\n")
            res = requests.get(url, headers=my_headers)

        data = res.text
        soup = bs4.BeautifulSoup(data, 'html.parser')

        expl_dict['单词'] = word
        try:
            expl_dict['音标'] = soup.find("span", attrs={"class": "phonetic"}).text
        except AttributeError:
            expl_dict['音标'] = ''
        try:
            expl_dict.setdefault("释义",
                                 "<br>".join(
                                     [li.text for li in soup.find(attrs={"class": "trans-container"}).find_all("li")]))
        except AttributeError:

            raise

        # -----------------collins-----------------------

        collins = soup.find('div', id="collinsResult")
        ls1 = []
        if collins:
            # for s in collins.descendants:
            #     if isinstance(s, bs4.element.NavigableString):
            #         if s.strip():
            #             ls1.append(s.strip())
            #
            # start_index = ls1.index(word)

            try:
                frequency = soup.find("span", title="使用频率")['class'][1][-1]
                frequency = int(frequency)
            except:
                frequency = 0

            if frequency:
                expl_dict['使用频率'] = "★" * frequency + "☆" * (5 - frequency)
            else:
                expl_dict['使用频率'] = "☆" * 5

            # Collins Major Trans
            collins_major_trans = collins.find("div", {"class": "collinsMajorTrans"})
            if collins_major_trans:
                trans_part = collins_major_trans.p
                cixing = trans_part.span.text
                english_explain = (" ".join([i.strip() for i in trans_part.text.split("\n")][2:])).strip()
                ying_ying_suiyi = "{}{}".format('<h class="h bg-r">{}</h> '.format(cixing)
                                                if cixing else "", english_explain)

                examples_part = soup.find("div", attrs={"class": "exampleLists"})
                if examples_part:
                    examples = examples_part.find("div", attrs={"class": "examples"})
                    example_strings = [p.string for p in examples.find_all("p")]

                    expl_dict.setdefault("例句", example_strings[0])
                    expl_dict.setdefault("例句翻译", example_strings[1])
                else:
                    expl_dict.setdefault("例句", "")
                    expl_dict.setdefault("例句翻译", "")

            else:
                ying_ying_suiyi = ""

            expl_dict.setdefault("英英释义", ying_ying_suiyi)

            try:
                rank_part = soup.find("span", attrs={"class": "via rank"})
                if rank_part:
                    expl_dict.setdefault("Rank", rank_part.string)
            except:
                expl_dict.setdefault("Rank", "")

        # 获取发音


        bin_mp3 = None
        tried_times = 10
        if not os.path.isdir(sound_dir):
            os.makedirs(sound_dir)

        sound_file = os.path.join(sound_dir, "{}.mp3".format(
            '{}_collins'.format(word) if addon_config.WordVoiceType == 'collins' else word)
                                  )

        expl_dict.setdefault("发音", os.path.basename(sound_file))

        youdao_voice_respond = lambda: requests.get("https://dict.youdao.com/dictvoice?audio={}&type=1".format(word),
                                                    headers=my_headers)

        while (not bin_mp3) and tried_times > 0 and not os.path.isfile(sound_file):
            print("Downloading sound - {}".format(word))
            if addon_config.WordVoiceType == 'collins':
                collins_host = "https://www.collinsdictionary.com"
                collins_word_url = collins_host + '/zh/dictionary/english/{}'.format(word)
                rsp = requests.get(collins_word_url, headers=my_headers)
                if 'spellcheck' in rsp.url or rsp.status_code != 200:
                    res = youdao_voice_respond()
                else:
                    collins_soup = bs4.BeautifulSoup(rsp.content.decode('utf-8', 'ignore'), 'html.parser')
                    sound_tag = collins_soup.find('a', attrs={'data-src-mp3': re.compile(r'/zh/sounds.+\.mp3')})
                    if sound_tag:
                        sound_url = collins_host + sound_tag['data-src-mp3']
                        res = requests.get(sound_url, headers=my_headers)
                    else:
                        res = youdao_voice_respond()
            else:  # Youdao
                res = youdao_voice_respond()

            if res.status_code == 200:
                if res.content.__len__():
                    bin_mp3 = res.content
                    with open(sound_file, "wb") as f:
                        f.write(bin_mp3)
                        break
                else:
                    print("No mp3 file contents for {}, try ... {}".format(word, tried_times + 1))
                tried_times -= 1

        expl_dict.setdefault("单词", "")
        expl_dict.setdefault("音标", "")
        expl_dict.setdefault("使用频率", "")
        expl_dict.setdefault("Rank", "")
        expl_dict.setdefault("英英释义", "")
        expl_dict.setdefault("释义", "")
        expl_dict.setdefault("发音", "")
        expl_dict.setdefault("例句", "")
        expl_dict.setdefault("例句翻译", "")
        return expl_dict
