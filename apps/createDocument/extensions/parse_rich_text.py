"""
专门解析富文本插件tinymce的html内容
"""
import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
import base64
import io
from docxtpl import InlineImage
from docx.shared import Mm

# text.replace('\xa0', ' '))
class RichParser:
    def __init__(self, rich_text):
        # 对原始html解析后的bs对象
        self.bs = BeautifulSoup(rich_text, 'html.parser')
        self.content = self.remove_n_in_contents()
        # 最终的解析后的列表
        self.data_list = []
        self.line_parse()

    # 1.函数：将self.bs.contents去掉\n，获取每行数据
    def remove_n_in_contents(self):
        content_list = []
        for line in self.bs.contents:
            if line != '\n':
                content_list.append(line)
        return content_list

    # 2.逐个遍历self.content，去掉table元素Tag对象单独解析
    def line_parse(self):
        for tag in self.content:
            if isinstance(tag, NavigableString):
                self.data_list.append(tag.text)
            elif isinstance(tag, Tag):
                if tag.name == 'p':
                    img_list = tag.find_all('img')
                    if len(img_list) > 0:
                        for img_item in img_list:
                            self.data_list.append(img_item.get('src'))
                    else:
                        self.data_list.append(tag.text)
                elif tag.name == 'table':
                    df_dict_list = self.parse_tag2list(tag)
                    self.data_list.append(df_dict_list)
                elif tag.name == 'div':
                    table_list = tag.find_all('table')
                    if len(table_list) > 0:
                        for table in table_list:
                            df_dict_list = self.parse_tag2list(table)
                            self.data_list.append(df_dict_list)

    # 3.1.辅助方法，将<table>的Tag对象转为[[]]二维列表格式
    def parse_tag2list(self, table_tag):
        # str(tag)可直接变成<table>xxx</table>
        pd_list = pd.read_html(str(table_tag))
        # 将dataframe变为数组
        df = pd_list[0]
        # 转为列表的列表（二维列表）
        # return df.values.tolist()
        return df.fillna('').T.reset_index().T.values.tolist()

    # 3.2.辅助方法，打印解析后列表
    def print_content(self):
        for line in self.data_list:
            print(line)

    # 4.最终方法，生成给docxtpl可用的列表 -> 注意需要传递DocxTemplate对象，在接口函数里面初始化的
    def get_final_list(self, doc):
        final_list = []
        for oneline in self.data_list:
            # 这里要单独处理下二维列表
            if isinstance(oneline, list):
                final_list.append({'isTable': True, 'data': oneline})
                continue
            if oneline.startswith("data:image/png;base64"):
                base64_bytes = base64.b64decode(oneline.replace("data:image/png;base64,", ""))
                # ~~~设置了固定宽度~~~
                final_list.append(InlineImage(doc, io.BytesIO(base64_bytes), width=Mm(115)))
            else:
                final_list.append(oneline)
        return final_list
