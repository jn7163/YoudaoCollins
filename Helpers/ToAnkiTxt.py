# using utf-8
import os
import re

from PyQt5.QtCore import QThread, pyqtSignal, QObject

from ..Helpers.Tools import chunks_by_el_count


class _OneWordDownloader(QThread):
    CompleteOne = pyqtSignal(bool)

    def __init__(self, words, soundDir, source_tag, kuozhan_dict=None):
        super(_OneWordDownloader, self).__init__()
        self.words = words
        self.soundDir = soundDir
        self.defines = []
        self.source_tag = source_tag
        self.kuozhan_dict = kuozhan_dict

    def run(self):

        from ..Helpers.Youdao import Youdao
        youdao = Youdao()
        for word_index, word in enumerate(self.words, 1):
            try:
                word = re.search("(\w+)(\s+)?", word).group(1).strip()
            except AttributeError:
                continue
            if not word: continue
            print("{}% - {} / {} - {}".format(
                round((word_index / self.words.__len__()) * 100, 2),
                word_index,
                self.words.__len__(),
                word
            ))
            try:
                word_dict = youdao.get_word_dict(word, self.soundDir)
            except Exception as exc:
                print("!! {} - {}".format(word, exc.__str__()))
                continue

            word_dict['扩展'] = self.kuozhan_dict[word] if self.kuozhan_dict else ""

            self.defines.append(
                "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                    word_dict['单词'],
                    word_dict['音标'],
                    word_dict['使用频率'],
                    word_dict['Rank'],
                    word_dict['英英释义'],
                    word_dict['释义'],
                    "[sound:{}]".format(word_dict['发音']),
                    word_dict['例句'],
                    word_dict['例句翻译'],
                    word_dict['扩展'],
                    self.source_tag,
                )
            )
            youdao.MarkWordImported(word)
            self.CompleteOne.emit(True)


class TransToAnkiText(QObject):
    CompletedOne = pyqtSignal()
    Complete = pyqtSignal(str)

    def __init__(self, ):
        super(TransToAnkiText, self).__init__()
        self.total_processes = []

    def trans_to_anki_text(self, input,
                           output_txt,
                           mp3_dir='mp3', source_tag=''):
        """

        :param input: file path; list of words; dict of {word: 扩展}
        :param output_txt:
        :param mp3_dir:
        :param source_tag:
        :return:
        """
        if isinstance(input, str) and os.path.isfile(input):
            with open(input, encoding="utf-8") as fr:
                total_lines = fr.readlines()
        elif isinstance(input, dict):
            total_lines = list(input.keys())
        else:
            total_lines = input

        if not os.path.isdir("Output"):
            os.makedirs("Output")
        output_txt = os.path.join("Output", output_txt)

        for words in chunks_by_el_count(total_lines, 50):
            proc = _OneWordDownloader(words, mp3_dir, source_tag, input if isinstance(input, dict) else None)
            self.total_processes.append(proc)
            proc.CompleteOne.connect(self.CompletedOne.emit)

        for proc in self.total_processes:
            proc.run()

        total_defs = []
        for proc in self.total_processes:
            proc.wait()
            total_defs.extend(proc.defines)

        if total_defs:
            with open(output_txt, "w", encoding="utf-8") as f2:
                f2.writelines(total_defs)
        else:
            if os.path.isfile(output_txt):
                os.remove(output_txt)

        self.Complete.emit(output_txt)


def GetWordsFromText(input_txt):
    """
    :param input_txt:
    :return:  {word: the left}
    """
    rDict = {}
    with open(input_txt, encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            pattern = "\w+\s\((\w+)\)(.+)"
            match = re.search(pattern, line)
            if match:
                word = match.group(1).strip()
                the_left = match.group(2)
            else:
                word = line.split(" ")[0]
                try:
                    the_left = " ".join(line.split(" ")[1:])
                except:
                    the_left=''
            rDict.setdefault(word, the_left.strip())
    return rDict
