import hashlib

import bs4
from requests import Session

headers = {
    'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, image/webp, */*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN, zh;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'Host': 'dict.youdao.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                       Chrome/48.0.2564.116 Safari/537.36'
}

_url = "http://dict.youdao.com/wordbook/"
_login_url = "http://account.youdao.com/login?service=dict&back_url=http://dict.youdao.com/wordbook/wordlist%3Fkeyfrom%3Dnull"


class _WordListRequester(Session):
    def __init__(self):
        super(_WordListRequester, self).__init__()

        self.last_res = None

    def login(self, username, password):
        password = hashlib.md5(password.encode('utf-8')).hexdigest()
        url = "https://logindict.youdao.com/login/acc/login"
        payload = "username=" + (username) + "&password=" + password + \
                  "&savelogin=1&app=web&tp=urstoken&cf=7&fr=1&ru=http%3A%2F%2Fdict.youdao.com%2Fwordbook%2Fwordlist%3Fkeyfrom%3Dnull&product=DICT&type=1&um=true&savelogin=1"

        url = url + '?' + payload
        self.last_res = self.request("GET", url, headers=headers)

    def GetWordList(self):

        if self.last_res.status_code != 200:
            raise Exception("[{}] - 有道单词本无法访问！".format(self.last_res.status_code))
        soup = bs4.BeautifulSoup(self.last_res.text)

        # find total pages
        words = []
        while 1:
            wordlist_part = soup.find("div", id='wordlist')

            if not wordlist_part:
                break
            words.extend([i['title'] for i in wordlist_part.find_all("div", attrs={"class": "word"})])
            next_page_part = soup.find("a", attrs={"class": "next-page"})
            if next_page_part and next_page_part.text == '下一页':
                soup = bs4.BeautifulSoup(self.request("GET",
                                                      url=_url + "/{}".format(next_page_part['href']),
                                                      headers=headers).text)
            else:
                break
        return words
