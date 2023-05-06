# This Python file uses the following encoding: utf-8

from lxml import etree
import requests
import random
from pypinyin import pinyin

class DataAcquisition():
    def __init__(self):
        super(DataAcquisition, self).__init__()


        self.poetryText = list()
        self.essayText = list()

        self.header = {
            "authority": "www.gushiwen.cn",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54"
            }

    def set_poetry(self):
        url = "https://www.gushiwen.cn/shiju/xiatian.aspx"


        req = requests.get(url= url, headers=self.header)
        if req.status_code == 200:

            html = etree.HTML(req.text)
            textStrin = list()
            textLen = int(len(html.xpath('//div[@class="cont"]/a[@target="_blank"]/text()'))/2)
            for i in range(textLen):
                i = i + 1
                text = html.xpath(f'//div[@class="cont"][{i}]/a[@target="_blank"]/text()')
                textStrin.append(text[0] + "——" + text[1])
        number = random.randint(1, 100)
        self.poetry = list(textStrin[number])
        return self.poetry

    def set_essay(self):
        number = random.randint(1, 22)
        url = f"https://www.bidushe.com/sanwen/{number}.html"

        req = requests.get(url= url, headers=self.header)
        req.encoding = "gbk"

        if req.status_code == 200:

            html = etree.HTML(req.text)

            title = html.xpath('//div[@class="content-left"]/h1/text()')
            text = html.xpath('//div[@class="content-left"]/div/p/text()')
            self.essayText = list("    "+"".join(title))
            self.essayText.append("\n")

            self.essayText = self.essayText+ list("  " + "".join(text))
        return self.essayText



    def set_pinyin(slft, text):
        pyText = pinyin(text)

        return pyText






if __name__ == '__main__':

    df = DataAcquisition()
