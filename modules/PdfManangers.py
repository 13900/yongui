# This Python file uses the following encoding: utf-8


from PySide6.QtCore import ( QObject, Signal, Slot )
from fpdf import FPDF
from .DataAcquisition import DataAcquisition
import re
import shutil

class PdfManangers(QObject):


    def __init__(self):
        super(PdfManangers, self).__init__()

        self.da = DataAcquisition()

        self.orientation = "P"
        self.format = "A4"

        self.set_default_header()

        # 定义内边距（单位为厘米）
        self.topMargin = 1.35
        self.bottomMargin = 1.35
        self.leftMargin = 1.5

        #控制文章和诗词的描字模式
        self.ep = 0

        #初始化文本内容
        self.text = list("")

        self.pinYinText = list("")

        self.essayNumber = 0

        self.spelling = 1

        #定义格子大小
        self.width = 1.5
        self.height = 1.5

        #定义没行间隔
        self.xInterval = 0
        self.yInterval = 0.3

        # 设置线条颜色和宽度
        self.rLine = 0
        self.gLine = 0
        self.bLine = 0

        # 描字颜色
        self.rTransparentFontColor = 153
        self.gTransparentFontColor = 153
        self.bTransparentFontColor = 153

        self.font = "resourceFiles/font/FangZhengKaiTi.ttf"
        self.fontSize = 35
        self.set_default()
        #默认字格
        self.space()

    @Slot(float, float)
    def set_grid_size(self, width, height):
        self.width = width
        self.height = height


    @Slot(int, int, int)
    def transparent_font(self, r, g, b):
        self.rTransparentFontColor = r
        self.gTransparentFontColor = g
        self.bTransparentFontColor = b

    @Slot(int, int, int)
    def set_line_color(self, r, g, b):
        self.rLine = r
        self.gLine = g
        self.bLine = b


    @Slot(int)
    def set_grid_mode(self, index=0):
        self.essayNumber = 0
        if index == 0:
            if self.ep == 1:
                self.text = ""
                self.ep = 0

            self.space()
        elif index == 1:
            if self.ep != 0:
                self.text = ""
                self.ep = 0
            self.tian_zi_ge()
        elif index == 7 or index == 9:
            if self.ep != 1:
                self.text = ""
                self.ep = 1
            self.essayNumber = 1
            self.spelling = 3
            self.tian_zi_ge()
        elif index == 2:
            if self.ep != 0:
                self.text = ""
                self.ep = 0
            self.meter_grid()
        elif index == 3:
            if self.ep != 0:
                self.text = ""
                self.ep = 0
            self.cross_grid()
        elif index == 4:
            if self.ep != 0:
                self.text = ""
                self.ep = 0
            self.back_to_palace_grid()
        elif index == 5:
            if self.ep != 0:
                self.text = ""
                self.ep = 0
            self.horizontal_word_post()
        elif index == 6:
            self.vertical_post()
        elif index == 8:
            if self.ep != 2:
                self.text = ""
                self.ep = 2

            self.pinyin()

    @Slot(int)
    def set_paper_mode(self, id):
        if id == 1:
            self.orientation = 'P'
            self.format = 'A4'
        else:
            self.orientation = 'L'
            self.format = 'A3'
        self.set_default_header()



    @Slot(str)
    def set_text_content(self, text):


        if self.ep == 2:
            chinese_pattern = re.compile('[^\u4e00-\u9fa5]+')
            py = list(chinese_pattern.sub('', text))
            self.pinYinText = self.da.set_pinyin(py)
            self.text = list(chinese_pattern.sub('', text))
        elif self.essayNumber == 1:
            self.ep = 1
            self.text = text
#            chinese_pattern = re.compile('[^a-zA-Z\u4e00-\u9fa5\s]+')
#            self.text = list(chinese_pattern.sub('', text))
        else:

            chinese_pattern = re.compile('[^\u4e00-\u9fa5]+')
            self.text = list(chinese_pattern.sub('', text))


    @Slot(int)
    def set_text_content1(self, index):

        if self.ep != 1:
            self.text = ""
            self.ep = 1

        if index == 0:
            self.text = self.da.set_essay()
        elif index == 1:
            self.text = self.da.set_poetry()

    @Slot(int)
    def set_font_size(self, x):
        self.fontSize = x
        self.pdf.set_font('font', '', self.fontSize)

    #设置字体
    @Slot(int)
    def set_custom_fonts(self, index):
        if index == 0:
            self.font = "resourceFiles/font/FangZhengKaiTi.ttf"
        elif index == 1:
            self.font = "resourceFiles/font/FangZhengShuSong.ttf"
        elif index == 2:
            self.font = "resourceFiles/font/HengShanMaoBiCaoShu.ttf"
        elif index == 3:
            self.font = "resourceFiles/font/JiZiJingDianLiShu.ttf"
        elif index == 4:
            self.font = "resourceFiles/font/SanJiXiaoZhuanShu.ttf"
        elif index == 5:
            self.font = "resourceFiles/font/YingZhangXingShu.ttf"
        self.pdf.set_font('font', '', self.fontSize)
        self.set_default_header()

    @Slot(int)
    def set_spelling(self, index):
        self.spelling = index

    def set_default_header(self):
        self.pdf = FPDF(orientation=self.orientation, unit="cm", format=self.format)
        self.pdf.add_page()

    def set_default(self):

        # 加载字体文件
        self.pdf.add_font('font', '', self.font, uni=True)

        # 设置字体
        self.pdf.set_font('font', '', self.fontSize)

        self.pdf.set_auto_page_break(auto=False, margin=0)
        self.pdf.set_xy(0, 0)


        self.pdf.set_top_margin(self.topMargin)

        self.pdf.set_top_margin(self.topMargin)
        self.pdf.set_draw_color(self.rLine, self.gLine, self.bLine)
        self.pdf.set_line_width(0.05)



    #绘制方格
    @Slot()
    def space(self):
        self.set_default()
        x = self.leftMargin
        y = self.topMargin

        w = int((21 - ((self.leftMargin * 2) + self.xInterval)) / self.width)
        h = int((self.pdf.h - ((self.topMargin * 2) + self.yInterval)) / self.height)
        count = 0
        textLen = len(self.text)
        xCountLen = int(w/2)
        pageMode = 0
        while True:
            if self.format == 'A3':
                pageMode = 2
            else:
                pageMode = 1
            for pm in range(pageMode):
                for y1 in range(h):

                    if y1 != 0:
                        y = (y1 * self.height) + (y1 * self.yInterval) + self.topMargin
                        count = count + 1
                    if (self.pdf.h - y) < (self.height + (self.yInterval * 2)) or (self.pdf.h - y) < self.topMargin:
                        break
                    xCount = 1
                    self.pdf.set_text_color(0,0,0)
                    for x1 in range(w):
                        if x1 != 0:
                            if pm == 1:
                                x = (x1  * self.width) + self.xInterval + self.leftMargin + 21
                            else:
                                x = (x1  * self.width) + self.xInterval + self.leftMargin
                            self.pdf.set_xy(x, y)
                            if (textLen > 0 and count < textLen) and self.spelling != 1:
                                if self.spelling == 2 and xCount < xCountLen:
                                    self.pdf.set_text_color(self.rTransparentFontColor, self.gTransparentFontColor, self.bTransparentFontColor)
                                    self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)
        #                            count = count + 1
                                    xCount = xCount + 1
                                elif self.spelling == 3:
                                    self.pdf.set_text_color(self.rTransparentFontColor, self.gTransparentFontColor, self.bTransparentFontColor)
                                    self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)
        #                            count = count + 1
                                else:
                                    self.pdf.cell(self.width, self.height, "",align="C", border=1)
                            else:
                                self.pdf.cell(self.width, self.height, "",align="C", border=1)
                        elif x1 == 0 and y1 != 0:
                            if pm == 1:
                                x = self.leftMargin + 21
                            else:
                                x = self.leftMargin
                            self.pdf.set_xy(x, y)
                            if (textLen > 0 and count < textLen):
                                self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)
        #                        count = count + 1
                            else:
                                self.pdf.cell(self.width, self.height, "",align="C", border=1)
                        else:
                            self.pdf.set_xy(x, y)
                            if textLen > 0 and count < textLen:
                                self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)
        #                        count = count + 1

                            else:
                                self.pdf.cell(self.width, self.height, "",align="C", border=1)


                if pm == 0:
                    x = self.leftMargin + 21
                    y = self.topMargin


            if count < textLen:
                self.pdf.add_page()
                x = self.leftMargin
                y = self.topMargin
                pageMode = 0
            else:
                break
        self.refreshPdf()

    #田字格
    @Slot()
    def tian_zi_ge(self):
        self.set_default()
        x = self.leftMargin
        y = self.topMargin

        w = int((21 - ((self.leftMargin * 2) + self.xInterval)) / self.width)
        h = int((self.pdf.h - ((self.topMargin * 2) + self.yInterval)) / self.height)

        count = 0
        textLen = len(self.text)
        xCountLen = int(w/2)
        pageMode = 0

        while True:
            if self.format == 'A3':
                pageMode = 2
            else:
                pageMode = 1
            for pm in range(pageMode):
                for y1 in range(h):
                    if y1 != 0:
                        y = (y1 * self.height) + (y1 * self.yInterval) + self.topMargin

                        count = count + 1
                    if (self.pdf.h - y) < (self.height + (self.yInterval * 2)) or (self.pdf.h - y) < self.topMargin:
                        break
                    xCount = 1
                    if self.ep == 1:
                        self.pdf.set_text_color(self.rTransparentFontColor, self.gTransparentFontColor, self.bTransparentFontColor)
                    else:
                        self.pdf.set_text_color(0,0,0)
                    for x1 in range(w):
                        if x1 != 0:
                            if pm == 1:
                                x = (x1  * self.width) + self.xInterval + self.leftMargin + 21
                            else:
                                x = (x1  * self.width) + self.xInterval + self.leftMargin
        #                    self.pdf.set_xy(x, y)
                            if (textLen > 0 and count < textLen) and self.spelling != 1:
                                if self.spelling == 2 and xCount < xCountLen:
                                    self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                    self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)
                                    self.pdf.set_text_color(self.rTransparentFontColor, self.gTransparentFontColor, self.bTransparentFontColor)
                                    self.pdf.set_xy(x, y)
                                    self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)

                                    if self.ep == 1:
                                        count = count + 1
                                    xCount = xCount + 1
                                elif self.spelling == 3:
                                    self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                    self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)
                                    self.pdf.set_text_color(self.rTransparentFontColor, self.gTransparentFontColor, self.bTransparentFontColor)
                                    self.pdf.set_xy(x, y)
                                    self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)

                                    if self.ep == 1:
                                        count = count + 1
                                else:
                                    self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                    self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)
                                    self.pdf.set_xy(x, y)
                                    self.pdf.cell(self.width, self.height, "",align="C", border=1)

                            else:
                                self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)
                                self.pdf.set_xy(x, y)
                                self.pdf.cell(self.width, self.height, "",align="C", border=1)
                        elif x1 == 0 and y1 != 0:
                            if pm == 1:
                                x = self.leftMargin + 21
                            else:
                                x = self.leftMargin
        #                    self.pdf.set_xy(x, y)
                            if (textLen > 0 and count < textLen):
                                self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)
                                self.pdf.set_xy(x, y)
                                self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)

                                if self.ep == 1:
                                    count = count + 1

                            else:
                                self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)
                                self.pdf.set_xy(x, y)
                                self.pdf.cell(self.width, self.height, "",align="C", border=1)
                        else:
        #                    self.pdf.set_xy(x, y)
                            if textLen > 0 and count < textLen:
                                self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)
                                self.pdf.set_xy(x, y)
                                self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)

                                if self.ep == 1:
                                    count = count + 1

                            else:
                                self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)
                                self.pdf.set_xy(x, y)
                                self.pdf.cell(self.width, self.height, "",align="C", border=1)
                if pm == 0:
                    x = self.leftMargin + 21
                    y = self.topMargin
            if count < textLen:
                self.pdf.add_page()
                x = self.leftMargin
                y = self.topMargin
                pageMode = 0
            else:
                break

        self.refreshPdf()




    #交叉字格
    @Slot()
    def cross_grid(self):
        self.set_default()
        x = self.leftMargin
        y = self.topMargin

        w = int((21 - ((self.leftMargin * 2) + self.xInterval)) / self.width)
        h = int((self.pdf.h - ((self.topMargin * 2) + self.yInterval)) / self.height)

        count = 0
        textLen = len(self.text)
        xCountLen = int(w/2)
        pageMode = 0

        while True:
            if self.format == 'A3':
                pageMode = 2
            else:
                pageMode = 1
            for pm in range(pageMode):
                for y1 in range(h):

                    if y1 != 0:
                        y = (y1 * self.height) + (y1 * self.yInterval) + self.topMargin
                        count = count + 1
                    if (29.7 - y) < (self.height + (self.yInterval * 2)) or (29.7 - y) < self.topMargin:
                        break
                    xCount = 1

                    self.pdf.set_text_color(0,0,0)
                    for x1 in range(w):

                        if x1 != 0:
                            if pm == 1:
                                x = (x1  * self.width) + self.xInterval + self.leftMargin + 21
                            else:
                                x = (x1  * self.width) + self.xInterval + self.leftMargin
                            self.pdf.set_xy(x, y)
                            if (textLen > 0 and count < textLen) and self.spelling != 1:
                                if self.spelling == 2 and xCount < xCountLen:
                                    self.pdf.dashed_line(x, y, x + self.width, y + self.height, 0.1, 0.1)
                                    self.pdf.dashed_line(x, y + self.height, x + self.width, y, 0.1, 0.1)
                                    self.pdf.set_xy(x, y)
                                    self.pdf.set_text_color(self.rTransparentFontColor, self.gTransparentFontColor, self.bTransparentFontColor)
                                    self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)
                #                            count = count + 1
                                    xCount = xCount + 1
                                elif self.spelling == 3:
                                    self.pdf.dashed_line(x, y, x + self.width, y + self.height, 0.1, 0.1)
                                    self.pdf.dashed_line(x, y + self.height, x + self.width, y, 0.1, 0.1)
                                    self.pdf.set_xy(x, y)
                                    self.pdf.set_text_color(self.rTransparentFontColor, self.gTransparentFontColor, self.bTransparentFontColor)
                                    self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)
                #                            count = count + 1
                                else:
                                    self.pdf.dashed_line(x, y, x + self.width, y + self.height, 0.1, 0.1)
                                    self.pdf.dashed_line(x, y + self.height, x + self.width, y, 0.1, 0.1)
                                    self.pdf.set_xy(x, y)
                                    self.pdf.cell(self.width, self.height, "",align="C", border=1)

                            else:
                                self.pdf.dashed_line(x, y, x + self.width, y + self.height, 0.1, 0.1)
                                self.pdf.dashed_line(x, y + self.height, x + self.width, y, 0.1, 0.1)
                                self.pdf.set_xy(x, y)
                                self.pdf.cell(self.width, self.height, "",align="C", border=1)
                        elif x1 == 0 and y1 != 0:
                            if pm == 1:
                                x = self.leftMargin + 21
                            else:
                                x = self.leftMargin
                            self.pdf.set_xy(x, y)
                            if (textLen > 0 and count < textLen):
                                self.pdf.dashed_line(x, y, x + self.width, y + self.height, 0.1, 0.1)
                                self.pdf.dashed_line(x, y + self.height, x + self.width, y, 0.1, 0.1)
                                self.pdf.set_xy(x, y)
                                self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)
                #                        count = count + 1
                            else:
                                self.pdf.dashed_line(x, y, x + self.width, y + self.height, 0.1, 0.1)
                                self.pdf.dashed_line(x, y + self.height, x + self.width, y, 0.1, 0.1)
                                self.pdf.set_xy(x, y)
                                self.pdf.cell(self.width, self.height, "",align="C", border=1)
                        else:
                            self.pdf.set_xy(x, y)
                            if textLen > 0 and count < textLen:
                                self.pdf.dashed_line(x, y, x + self.width, y + self.height, 0.1, 0.1)
                                self.pdf.dashed_line(x, y + self.height, x + self.width, y, 0.1, 0.1)
                                self.pdf.set_xy(x, y)
                                self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)
                #                        count = count + 1

                            else:
                                self.pdf.dashed_line(x, y, x + self.width, y + self.height, 0.1, 0.1)
                                self.pdf.dashed_line(x, y + self.height, x + self.width, y, 0.1, 0.1)
                                self.pdf.set_xy(x, y)
                                self.pdf.cell(self.width, self.height, "",align="C", border=1)
                if pm == 0:
                    x = self.leftMargin + 21
                    y = self.topMargin
            if count < textLen:
                self.pdf.add_page()
                x = self.leftMargin
                y = self.topMargin
                pageMode = 0
            else:
                break

        self.refreshPdf()

    #米字格
    @Slot()
    def meter_grid(self):
        self.set_default()
        x = self.leftMargin
        y = self.topMargin

        w = int((21 - ((self.leftMargin * 2) + self.xInterval)) / self.width)
        h = int((self.pdf.h - ((self.topMargin * 2) + self.yInterval)) / self.height)

        count = 0
        textLen = len(self.text)
        xCountLen = int(w/2)
        pageMode = 0

        while True:
            if self.format == 'A3':
                pageMode = 2
            else:
                pageMode = 1

            for pm in range(pageMode):
                for y1 in range(h):

                    if y1 != 0:
                        y = (y1 * self.height) + (y1 * self.yInterval) + self.topMargin
                        count = count + 1
                    if (29.7 - y) < (self.height + (self.yInterval * 2)) or (29.7 - y) < self.topMargin:
                        break
                    xCount = 1
                    self.pdf.set_text_color(0,0,0)
                    for x1 in range(w):
                        if x1 != 0:
                            if pm == 1:
                                x = (x1  * self.width) + self.xInterval + self.leftMargin + 21
                            else:
                                x = (x1  * self.width) + self.xInterval + self.leftMargin
                            self.pdf.set_xy(x, y)
                            if (textLen > 0 and count < textLen) and self.spelling != 1:
                                if self.spelling == 2 and xCount < xCountLen:
                                    self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                    self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)
                                    self.pdf.dashed_line(x, y, x + self.width, y + self.height, 0.1, 0.1)
                                    self.pdf.dashed_line(x, y + self.height, x + self.width, y, 0.1, 0.1)
                                    self.pdf.set_xy(x, y)
                                    self.pdf.set_text_color(self.rTransparentFontColor, self.gTransparentFontColor, self.bTransparentFontColor)
                                    self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)
                #                            count = count + 1
                                    xCount = xCount + 1
                                elif self.spelling == 3:
                                    self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                    self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)
                                    self.pdf.dashed_line(x, y, x + self.width, y + self.height, 0.1, 0.1)
                                    self.pdf.dashed_line(x, y + self.height, x + self.width, y, 0.1, 0.1)
                                    self.pdf.set_xy(x, y)
                                    self.pdf.set_text_color(self.rTransparentFontColor, self.gTransparentFontColor, self.bTransparentFontColor)
                                    self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)
                #                            count = count + 1
                                else:
                                    self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                    self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)
                                    self.pdf.dashed_line(x, y, x + self.width, y + self.height, 0.1, 0.1)
                                    self.pdf.dashed_line(x, y + self.height, x + self.width, y, 0.1, 0.1)
                                    self.pdf.set_xy(x, y)
                                    self.pdf.cell(self.width, self.height, "",align="C", border=1)

                            else:
                                self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)
                                self.pdf.dashed_line(x, y, x + self.width, y + self.height, 0.1, 0.1)
                                self.pdf.dashed_line(x, y + self.height, x + self.width, y, 0.1, 0.1)
                                self.pdf.set_xy(x, y)
                                self.pdf.cell(self.width, self.height, "",align="C", border=1)
                        elif x1 == 0 and y1 != 0:
                            if pm == 1:
                                x = self.leftMargin + 21
                            else:
                                x = self.leftMargin
                            self.pdf.set_xy(x, y)
                            if (textLen > 0 and count < textLen):
                                self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)
                                self.pdf.dashed_line(x, y, x + self.width, y + self.height, 0.1, 0.1)
                                self.pdf.dashed_line(x, y + self.height, x + self.width, y, 0.1, 0.1)
                                self.pdf.set_xy(x, y)
                                self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)
                #                        count = count + 1
                            else:
                                self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)
                                self.pdf.dashed_line(x, y, x + self.width, y + self.height, 0.1, 0.1)
                                self.pdf.dashed_line(x, y + self.height, x + self.width, y, 0.1, 0.1)
                                self.pdf.set_xy(x, y)
                                self.pdf.cell(self.width, self.height, "",align="C", border=1)
                        else:
                            self.pdf.set_xy(x, y)
                            if textLen > 0 and count < textLen:
                                self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)
                                self.pdf.dashed_line(x, y, x + self.width, y + self.height, 0.1, 0.1)
                                self.pdf.dashed_line(x, y + self.height, x + self.width, y, 0.1, 0.1)
                                self.pdf.set_xy(x, y)
                                self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)
                #                        count = count + 1

                            else:
                                self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)
                                self.pdf.dashed_line(x, y, x + self.width, y + self.height, 0.1, 0.1)
                                self.pdf.dashed_line(x, y + self.height, x + self.width, y, 0.1, 0.1)
                                self.pdf.set_xy(x, y)
                                self.pdf.cell(self.width, self.height, "",align="C", border=1)
                if pm == 0:
                    x = self.leftMargin + 21
                    y = self.topMargin

            if count < textLen:
                self.pdf.add_page()
                x = self.leftMargin
                y = self.topMargin
                pageMode = 0
            else:
                break

        self.refreshPdf()

    #回宫格
    @Slot()
    def back_to_palace_grid(self):
         self.set_default()
         x = self.leftMargin
         y = self.topMargin

         w = int((21 - ((self.leftMargin * 2) + self.xInterval)) / self.width)
         h = int((self.pdf.h - ((self.topMargin * 2) + self.yInterval)) / self.height)

         count = 0
         textLen = len(self.text)
         xCountLen = int(w/2)
         pageMode = 0

         while True:
             if self.format == 'A3':
                 pageMode = 2
             else:
                 pageMode = 1
             for pm in range(pageMode):
                 for y1 in range(h):

                    if y1 != 0:
                        y = (y1 * self.height) + (y1 * self.yInterval) + self.topMargin
                        count = count + 1
                    if (29.7 - y) < (self.height + (self.yInterval * 2)) or (29.7 - y) < self.topMargin:
                        break
                    xCount = 1
                    self.pdf.set_text_color(0,0,0)
                    for x1 in range(w):

                        if x1 != 0:
                            if pm == 1:
                                x = (x1  * self.width) + self.xInterval + self.leftMargin + 21
                            else:
                                x = (x1  * self.width) + self.xInterval + self.leftMargin
                            self.pdf.set_xy(x, y)
                            if (textLen > 0 and count < textLen) and self.spelling != 1:
                                if self.spelling == 2 and xCount < xCountLen:
                                    self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                    self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)

                                    self.pdf.dashed_line(x + (self.width / 4), y + (self.height / 8), x + (self.width / 4), y + ((self.height / 8) * 7 ), 0.1, 0.1)
                                    self.pdf.dashed_line(x + (self.width / 4), y + (self.height / 8), x + ((self.width / 4) * 3), y + (self.height / 8 ), 0.1, 0.1)
                                    self.pdf.dashed_line(x + (self.width / 4), y + ((self.height / 8) * 7), x + ((self.width / 4) * 3), y + ((self.height / 8) * 7), 0.1, 0.1)
                                    self.pdf.dashed_line(x + ((self.width / 4) * 3), y + (self.height / 8 ), x + ((self.width / 4) * 3), y + ((self.height / 8 ) * 7), 0.1, 0.1)
                                    self.pdf.set_xy(x, y)
                                    self.pdf.set_text_color(self.rTransparentFontColor, self.gTransparentFontColor, self.bTransparentFontColor)
                                    self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)
                #                            count = count + 1
                                    xCount = xCount + 1
                                elif self.spelling == 3:
                                    self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                    self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)

                                    self.pdf.dashed_line(x + (self.width / 4), y + (self.height / 8), x + (self.width / 4), y + ((self.height / 8) * 7 ), 0.1, 0.1)
                                    self.pdf.dashed_line(x + (self.width / 4), y + (self.height / 8), x + ((self.width / 4) * 3), y + (self.height / 8 ), 0.1, 0.1)
                                    self.pdf.dashed_line(x + (self.width / 4), y + ((self.height / 8) * 7), x + ((self.width / 4) * 3), y + ((self.height / 8) * 7), 0.1, 0.1)
                                    self.pdf.dashed_line(x + ((self.width / 4) * 3), y + (self.height / 8 ), x + ((self.width / 4) * 3), y + ((self.height / 8 ) * 7), 0.1, 0.1)
                                    self.pdf.set_xy(x, y)

                                    self.pdf.set_text_color(self.rTransparentFontColor, self.gTransparentFontColor, self.bTransparentFontColor)
                                    self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)
                #                            count = count + 1
                                else:
                                    self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                    self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)

                                    self.pdf.dashed_line(x + (self.width / 4), y + (self.height / 8), x + (self.width / 4), y + ((self.height / 8) * 7 ), 0.1, 0.1)
                                    self.pdf.dashed_line(x + (self.width / 4), y + (self.height / 8), x + ((self.width / 4) * 3), y + (self.height / 8 ), 0.1, 0.1)
                                    self.pdf.dashed_line(x + (self.width / 4), y + ((self.height / 8) * 7), x + ((self.width / 4) * 3), y + ((self.height / 8) * 7), 0.1, 0.1)
                                    self.pdf.dashed_line(x + ((self.width / 4) * 3), y + (self.height / 8 ), x + ((self.width / 4) * 3), y + ((self.height / 8 ) * 7), 0.1, 0.1)
                                    self.pdf.set_xy(x, y)

                                    self.pdf.cell(self.width, self.height, "",align="C", border=1)

                            else:
                                self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)

                                self.pdf.dashed_line(x + (self.width / 4), y + (self.height / 8), x + (self.width / 4), y + ((self.height / 8) * 7 ), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 4), y + (self.height / 8), x + ((self.width / 4) * 3), y + (self.height / 8 ), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 4), y + ((self.height / 8) * 7), x + ((self.width / 4) * 3), y + ((self.height / 8) * 7), 0.1, 0.1)
                                self.pdf.dashed_line(x + ((self.width / 4) * 3), y + (self.height / 8 ), x + ((self.width / 4) * 3), y + ((self.height / 8 ) * 7), 0.1, 0.1)
                                self.pdf.set_xy(x, y)

                                self.pdf.cell(self.width, self.height, "",align="C", border=1)
                        elif x1 == 0 and y1 != 0:
                            if pm == 1:
                                x = self.leftMargin + 21
                            else:
                                x = self.leftMargin
                            self.pdf.set_xy(x, y)
                            if (textLen > 0 and count < textLen):
                                self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)

                                self.pdf.dashed_line(x + (self.width / 4), y + (self.height / 8), x + (self.width / 4), y + ((self.height / 8) * 7 ), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 4), y + (self.height / 8), x + ((self.width / 4) * 3), y + (self.height / 8 ), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 4), y + ((self.height / 8) * 7), x + ((self.width / 4) * 3), y + ((self.height / 8) * 7), 0.1, 0.1)
                                self.pdf.dashed_line(x + ((self.width / 4) * 3), y + (self.height / 8 ), x + ((self.width / 4) * 3), y + ((self.height / 8 ) * 7), 0.1, 0.1)
                                self.pdf.set_xy(x, y)

                                self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)
                #                        count = count + 1
                            else:
                                self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)

                                self.pdf.dashed_line(x + (self.width / 4), y + (self.height / 8), x + (self.width / 4), y + ((self.height / 8) * 7 ), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 4), y + (self.height / 8), x + ((self.width / 4) * 3), y + (self.height / 8 ), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 4), y + ((self.height / 8) * 7), x + ((self.width / 4) * 3), y + ((self.height / 8) * 7), 0.1, 0.1)
                                self.pdf.dashed_line(x + ((self.width / 4) * 3), y + (self.height / 8 ), x + ((self.width / 4) * 3), y + ((self.height / 8 ) * 7), 0.1, 0.1)
                                self.pdf.set_xy(x, y)

                                self.pdf.cell(self.width, self.height, "",align="C", border=1)
                        else:
                            self.pdf.set_xy(x, y)
                            if textLen > 0 and count < textLen:
                                self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)

                                self.pdf.dashed_line(x + (self.width / 4), y + (self.height / 8), x + (self.width / 4), y + ((self.height / 8) * 7 ), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 4), y + (self.height / 8), x + ((self.width / 4) * 3), y + (self.height / 8 ), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 4), y + ((self.height / 8) * 7), x + ((self.width / 4) * 3), y + ((self.height / 8) * 7), 0.1, 0.1)
                                self.pdf.dashed_line(x + ((self.width / 4) * 3), y + (self.height / 8 ), x + ((self.width / 4) * 3), y + ((self.height / 8 ) * 7), 0.1, 0.1)
                                self.pdf.set_xy(x, y)

                                self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)
                #                        count = count + 1

                            else:
                                self.pdf.dashed_line(x , y + (self.height / 2), x + self.width, y + (self.height / 2), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 2) , y, x + (self.width / 2), y + self.height, 0.1, 0.1)

                                self.pdf.dashed_line(x + (self.width / 4), y + (self.height / 8), x + (self.width / 4), y + ((self.height / 8) * 7 ), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 4), y + (self.height / 8), x + ((self.width / 4) * 3), y + (self.height / 8 ), 0.1, 0.1)
                                self.pdf.dashed_line(x + (self.width / 4), y + ((self.height / 8) * 7), x + ((self.width / 4) * 3), y + ((self.height / 8) * 7), 0.1, 0.1)
                                self.pdf.dashed_line(x + ((self.width / 4) * 3), y + (self.height / 8 ), x + ((self.width / 4) * 3), y + ((self.height / 8 ) * 7), 0.1, 0.1)
                                self.pdf.set_xy(x, y)

                                self.pdf.cell(self.width, self.height, "",align="C", border=1)
                 if pm == 0:
                    x = self.leftMargin + 21
                    y = self.topMargin

             if count < textLen:
                self.pdf.add_page()
                x = self.leftMargin
                y = self.topMargin
                pageMode = 0
             else:
                break

         self.refreshPdf()

     #竖字帖
    @Slot()
    def vertical_post(self):

        self.topMargin = 1.5
        self.leftMargin = 1.2

        if self.width == 1.5:
            x = 1.95
            y = 1.95
        elif self.width == 2:
            x = 1.2
            y = 1.5
        else:
            y = 1.75
            x = 1.75
        rWidth = self.pdf.w - (x * 2)
        rHeight = self.pdf.h - (y * 2)
        self.pdf.set_line_width(0.1)
        self.pdf.rect(x, y, rWidth, rHeight)
        r1 = x + 0.3
        r2 = y + 0.3
        r1Width = self.pdf.w - (r1 * 2)
        r2Height = self.pdf.h - (r2 * 2)
        self.pdf.set_line_width(0.05)
        self.pdf.rect(r1, r2, r1Width, r2Height)
        lineNumber = int(r1Width / self.width)
        for i in range(lineNumber):
            r1 = r1 + self.width
            self.pdf.line(r1, r2, r1, r2 + r2Height)
        self.refreshPdf()


    #横字贴
    @Slot()
    def horizontal_word_post(self):

        if self.width == 1.5:
            x = 1.8
            y = 1.8
        else:
            x = 1.55
            y = 1.55
        rWidth = self.pdf.w - (x * 2)
        rHeight = self.pdf.h - (y * 2)
        self.pdf.set_line_width(0.1)
        self.pdf.rect(x, y, rWidth, rHeight)
        r1 = x + 0.3
        r2 = y + 0.3
        r1Width = self.pdf.w - (r1 * 2)
        r2Height = self.pdf.h - (r2 * 2)
        self.pdf.set_line_width(0.05)
        self.pdf.rect(r1, r2, r1Width, r2Height)
        lineNumber = int(r2Height / self.width)
        for i in range(lineNumber):
            r2 = r2 + self.width

            self.pdf.line(r1, r2, r1 + r1Width, r2)

        self.refreshPdf()




    #拼音字帖
    @Slot()
    def pinyin(self):

        self.set_default()
        x = self.leftMargin
        y = self.topMargin

        w = int((21 - ((self.leftMargin * 2) + self.xInterval)) / self.width)
        h = int((self.pdf.h - ((self.topMargin * 2) + self.yInterval)) / self.height)

        count = 0
        textLen = len(self.text)
        xCountLen = int(w/2)
        pageMode = 0

        while True:
            if self.format == 'A3':
                pageMode = 2
            else:
                pageMode = 1

            for pm in range(pageMode):
                for y1 in range(h):
                        if y1 != 0:
                            y = (y1 * (self.height + (self.height / 2))) + (y1 * self.yInterval) + self.topMargin
                            count = count + 1
                        if (self.pdf.h - y) < (self.height + (self.yInterval * 2)) or (self.pdf.h - y) < self.topMargin:
                            break
                        xCount = 1
                        self.pdf.set_text_color(0,0,0)
                        for x1 in range(w):
                            if x1 != 0:
                                if pm == 1:
                                    x = (x1  * self.width) + self.xInterval + self.leftMargin + 21
                                else:
                                    x = (x1  * self.width) + self.xInterval + self.leftMargin
            #                    self.pdf.set_xy(x, y)
                                if (textLen > 0 and count < textLen) and self.spelling != 1:
                                    if self.spelling == 2 and xCount < xCountLen:
                                        self.pdf.line(x, y, x + self.width, y)
                                        self.pdf.set_line_width(0.01)
                                        self.pdf.dashed_line(x, y + ((self.height / 2) /3), x + self.width, y + ((self.height / 2) / 3), 0.1, 0.1)
                                        self.pdf.dashed_line(x, y + (((self.height / 2) /3)* 2), x + self.width, y + (((self.height / 2) /3)* 2), 0.1, 0.1)

                                        self.pdf.dashed_line(x , y + self.height, x + self.width, y + self.height, 0.1, 0.1)
                                        self.pdf.dashed_line(x + (self.width / 2) , y + (self.height / 2), x + (self.width / 2), y + (self.height / 2) + self.height, 0.1, 0.1)
                                        self.pdf.set_line_width(0.05)

                                        self.pdf.set_text_color(self.rTransparentFontColor, self.gTransparentFontColor, self.bTransparentFontColor)

                                        self.pdf.set_xy(x, y - 0.03)
                                        self.pdf.set_font_size(15)
                                        self.pdf.cell(self.width, (self.height / 2), self.pinYinText[count][0],align="C")

                                        self.pdf.set_font_size(self.fontSize)


                                        self.pdf.set_xy(x, y + (self.height / 2))
                                        self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)
                    #                            count = count + 1
                                        xCount = xCount + 1
                                    elif self.spelling == 3:
                                        self.pdf.line(x, y, x + self.width, y)
                                        self.pdf.set_line_width(0.01)
                                        self.pdf.dashed_line(x, y + ((self.height / 2) /3), x + self.width, y + ((self.height / 2) / 3), 0.1, 0.1)
                                        self.pdf.dashed_line(x, y + (((self.height / 2) /3)* 2), x + self.width, y + (((self.height / 2) /3)* 2), 0.1, 0.1)

                                        self.pdf.dashed_line(x , y + self.height, x + self.width, y + self.height, 0.1, 0.1)
                                        self.pdf.dashed_line(x + (self.width / 2) , y + (self.height / 2), x + (self.width / 2), y + (self.height / 2) + self.height, 0.1, 0.1)
                                        self.pdf.set_line_width(0.05)

                                        self.pdf.set_text_color(self.rTransparentFontColor, self.gTransparentFontColor, self.bTransparentFontColor)

                                        self.pdf.set_xy(x, y - 0.03)
                                        self.pdf.set_font_size(15)
                                        self.pdf.cell(self.width, (self.height / 2), self.pinYinText[count][0],align="C")

                                        self.pdf.set_font_size(self.fontSize)

                                        self.pdf.set_xy(x, y + (self.height / 2))
                                        self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)
                    #                            count = count + 1
                                    else:
                                        self.pdf.line(x, y, x + self.width, y)
                                        self.pdf.set_line_width(0.01)
                                        self.pdf.dashed_line(x, y + ((self.height / 2) /3), x + self.width, y + ((self.height / 2) / 3), 0.1, 0.1)
                                        self.pdf.dashed_line(x, y + (((self.height / 2) /3)* 2), x + self.width, y + (((self.height / 2) /3)* 2), 0.1, 0.1)

                                        self.pdf.dashed_line(x , y + self.height, x + self.width, y + self.height, 0.1, 0.1)
                                        self.pdf.dashed_line(x + (self.width / 2) , y + (self.height / 2), x + (self.width / 2), y + (self.height / 2) + self.height, 0.1, 0.1)
                                        self.pdf.set_line_width(0.05)

                                        self.pdf.set_xy(x, y)
                                        self.pdf.cell(self.width, self.height, "",align="C")

                                        self.pdf.set_xy(x, y + (self.height / 2))
                                        self.pdf.cell(self.width, self.height, "",align="C", border=1)

                                else:
                                    self.pdf.line(x, y, x + self.width, y)
                                    self.pdf.set_line_width(0.01)
                                    self.pdf.dashed_line(x, y + ((self.height / 2) /3), x + self.width, y + ((self.height / 2) / 3), 0.1, 0.1)
                                    self.pdf.dashed_line(x, y + (((self.height / 2) /3)* 2), x + self.width, y + (((self.height / 2) /3)* 2), 0.1, 0.1)

                                    self.pdf.dashed_line(x , y + self.height, x + self.width, y + self.height, 0.1, 0.1)
                                    self.pdf.dashed_line(x + (self.width / 2) , y + (self.height / 2), x + (self.width / 2), y + (self.height / 2) + self.height, 0.1, 0.1)
                                    self.pdf.set_line_width(0.05)

                                    self.pdf.set_xy(x, y)
                                    self.pdf.cell(self.width, self.height, "",align="C")

                                    self.pdf.set_xy(x, y + (self.height / 2))
                                    self.pdf.cell(self.width, self.height, "",align="C", border=1)
                            elif x1 == 0 and y1 != 0:
                                if pm == 1:
                                    x = self.leftMargin + 21
                                else:
                                    x = self.leftMargin
            #                    self.pdf.set_xy(x, y)
                                if (textLen > 0 and count < textLen):
                                    self.pdf.line(x, y, x + self.width, y)
                                    self.pdf.set_line_width(0.01)
                                    self.pdf.dashed_line(x, y + ((self.height / 2) /3), x + self.width, y + ((self.height / 2) / 3), 0.1, 0.1)
                                    self.pdf.dashed_line(x, y + (((self.height / 2) /3)* 2), x + self.width, y + (((self.height / 2) /3)* 2), 0.1, 0.1)

                                    self.pdf.dashed_line(x , y + self.height, x + self.width, y + self.height, 0.1, 0.1)
                                    self.pdf.dashed_line(x + (self.width / 2) , y + (self.height / 2), x + (self.width / 2), y + (self.height / 2) + self.height, 0.1, 0.1)
                                    self.pdf.set_line_width(0.05)

                                    self.pdf.set_xy(x, y - 0.03)
                                    self.pdf.set_font_size(15)
                                    self.pdf.cell(self.width, (self.height / 2), self.pinYinText[count][0],align="C")

                                    self.pdf.set_font_size(self.fontSize)

                                    self.pdf.set_xy(x, y + (self.height / 2))
                                    self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)
                    #                        count = count + 1
                                else:
                                    self.pdf.line(x, y, x + self.width, y)
                                    self.pdf.set_line_width(0.01)
                                    self.pdf.dashed_line(x, y + ((self.height / 2) /3), x + self.width, y + ((self.height / 2) / 3), 0.1, 0.1)
                                    self.pdf.dashed_line(x, y + (((self.height / 2) /3)* 2), x + self.width, y + (((self.height / 2) /3)* 2), 0.1, 0.1)

                                    self.pdf.dashed_line(x , y + self.height, x + self.width, y + self.height, 0.1, 0.1)
                                    self.pdf.dashed_line(x + (self.width / 2) , y + (self.height / 2), x + (self.width / 2), y + (self.height / 2) + self.height, 0.1, 0.1)
                                    self.pdf.set_line_width(0.05)

                                    self.pdf.set_xy(x, y)
                                    self.pdf.cell(self.width, self.height, "",align="C")

                                    self.pdf.set_xy(x, y + (self.height / 2))
                                    self.pdf.cell(self.width, self.height, "",align="C", border=1)
                            else:
            #                    self.pdf.set_xy(x, y)
                                if textLen > 0 and count < textLen:
                                    self.pdf.line(x, y, x + self.width, y)
                                    self.pdf.set_line_width(0.01)
                                    self.pdf.dashed_line(x, y + ((self.height / 2) /3), x + self.width, y + ((self.height / 2) / 3), 0.1, 0.1)
                                    self.pdf.dashed_line(x, y + (((self.height / 2) /3)* 2), x + self.width, y + (((self.height / 2) /3)* 2), 0.1, 0.1)

                                    self.pdf.dashed_line(x , y + self.height, x + self.width, y + self.height, 0.1, 0.1)
                                    self.pdf.dashed_line(x + (self.width / 2) , y + (self.height / 2), x + (self.width / 2), y + (self.height / 2) + self.height, 0.1, 0.1)
                                    self.pdf.set_line_width(0.05)

                                    self.pdf.set_xy(x, y - 0.03)
                                    self.pdf.set_font_size(15)
                                    self.pdf.cell(self.width, (self.height / 2), self.pinYinText[count][0],align="C")

                                    self.pdf.set_font_size(self.fontSize)
                                    self.pdf.set_xy(x, y + (self.height / 2))
                                    self.pdf.cell(self.width, self.height, self.text[count],align="C", border=1)
                    #                        count = count + 1

                                else:
                                    self.pdf.line(x, y, x + self.width, y)
                                    self.pdf.set_line_width(0.01)
                                    self.pdf.dashed_line(x, y + ((self.height / 2) /3), x + self.width, y + ((self.height / 2) / 3), 0.1, 0.1)
                                    self.pdf.dashed_line(x, y + (((self.height / 2) /3)* 2), x + self.width, y + (((self.height / 2) /3)* 2), 0.1, 0.1)

                                    self.pdf.dashed_line(x , y + self.height, x + self.width, y + self.height, 0.1, 0.1)
                                    self.pdf.dashed_line(x + (self.width / 2) , y + (self.height / 2), x + (self.width / 2), y + (self.height / 2) + self.height, 0.1, 0.1)
                                    self.pdf.set_line_width(0.05)

                                    self.pdf.set_xy(x, y)
                                    self.pdf.cell(self.width, self.height, "",align="C")

                                    self.pdf.set_xy(x, y + (self.height / 2))
                                    self.pdf.cell(self.width, self.height, "",align="C", border=1)
                if pm == 0:
                    x = self.leftMargin + 21
                    y = self.topMargin


            if count < textLen:
                self.pdf.add_page()
                x = self.leftMargin
                y = self.topMargin
                pageMode = 0
            else:
                break

        self.refreshPdf()



    #刷新 PDF 文件
    def refreshPdf(self):

        self.pdf.output("resourceFiles/you_gui.pdf")

        self.set_default_header()
        self.set_default()

    @Slot(str)
    def export_file(self, filePath):
        path = filePath.replace("file:///", "")
        shutil.copy("resourceFiles/you_gui.pdf", path)

