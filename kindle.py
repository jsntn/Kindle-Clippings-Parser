# -*- coding: utf-8 -*-
from __future__ import print_function

import re
import os
import shutil


class book:
    def __init__(self, name, author):
        self.name = name
        self.author = author
        self.contents = []

    def add(self, pos, content):
        if len(self.contents) > 0:
            if self.contents[-1][0] == pos:
                del self.contents[-1]
        self.contents.append((pos, content))

def strip(func):
    """
    将函数的参数字符串掐头去尾
    """
    def wrapper(*args, **kwargs):
        # 目前只判断 1 个参数的情况，未来可以扩展为多个
        if(len(args) == 1 and isinstance(args[0], str)):
            striped_arg = args[0].strip()
        else:
            raise AttributeError
        return func(striped_arg)
    return wrapper

@strip
def handleBookName(text):
    """
    提取书本名称及作者
    """

    if ' ' in text:
        name_part, author_part = text.split(' ', 1)
        author_regex = r'\((.*?)\)$'
        author = re.search(author_regex, author_part).group(1)
    else:
        name_part = text
        author = ''

    name_regex = r'^(.*)' # r'[\ufeff](.*)'
    special_name_regex = r'[:](.*?)[ (]'

    if not re.search(special_name_regex, name_part):
        name_found = re.search(name_regex, name_part)
        if name_found:
            name = name_found.group(1)
        else:
            raise ValueError('未能匹配到书本名称')
    else:
        name = special_name_res.group(1)

    return name.strip(), author.strip()

@strip
def handlePos(text):
    """
    提取标注位置
    """
    pos_regex = r'#(\d*)'
    pos_found = re.search(pos_regex, text)
    if pos_found:
        return pos_found.group(1)
    else:
        return 0  # 无法匹配出位置，以 0 代替

@strip
def handleContent(text):
    """
    提取标注内容
    """
    text = text.strip()
    if not text:
        return ''

    # 检查起始字符
    if text[0] in {'，', '：'}:
        text = text[1:]

    # 检查末尾字符标点
    if text[-1] in {'，', '：'}:
        text = text[:-1].join('。')
    elif text[-1] not in {'。', '？', '！', '”'}:
        text = text.join('。')

    return re.sub(r'(\s+)', '\n', text)

bookList = {}
srcFile = open('My Clippings.txt', 'r', encoding='utf-8')
allPieces = srcFile.read().split("==========\n")
del allPieces[-1]

for paragraph in allPieces:
    name_line, pos_line, _, content_block = paragraph.split('\n', 3)
    bookname, author = handleBookName(name_line)
    pos = handlePos(pos_line)
    content = handleContent(content_block)

    if len(content) > 3:
        if bookname not in bookList:
            the_book = book(bookname, author)
            the_book.add(pos, content)
            bookList[bookname] = the_book
        else:
            bookList[bookname].add(pos, content)


for book in bookList.values():

    bookname = book.name
    print("Generating ...", book.name)

    if os.path.exists(bookname):
        shutil.rmtree(bookname)
        os.makedirs(bookname)
    else:
        os.makedirs(bookname)
    file = open(bookname + '/' + bookname + '.txt', 'w', encoding='utf-8')

    for content in book.contents:
        file.write(content[1] + '\n\n')
    file.close()
print("Done.")
