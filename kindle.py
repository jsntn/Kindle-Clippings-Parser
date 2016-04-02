#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import re
import os
import shutil

OUTPUT_DIR = 'output' # 输出文件夹名
MIN_CONTENT_LENGTH = 3 # 摘录内容最小可接受长度


class book:
    """
    图书类，每本书有 书名（name），作者（author），摘录内容列表（contents）
    摘录内容列表中，每个元素是键为 pos 和 content 的词典
    """
    def __init__(self, name, author, pos, content):
        self.name, self.author = name, author
        self.contents = [{'pos': pos, 'content': content}]

    def add(self, pos, content):
        """
        向图书添加新的摘录内容及其位置
        """
        if self.contents:
            if self.contents[-1]['pos'] == pos:
                del self.contents[-1]
        self.contents.append({'pos': pos, 'content': content})


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
def extract_title(text):
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

    name_regex = r'^(.*)'
    special_name_regex = r'[:](.*?)[ (]'

    special_name_found = re.search(special_name_regex, name_part)
    if special_name_found:
        name = special_name_found.group(1)
    else:
        name_found = re.search(name_regex, name_part)
        if name_found:
            name = name_found.group(1)
        else:
            raise ValueError('未能匹配到书本名称')

    return name.strip(), author.strip()


@strip
def extract_position(text):
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
def extract_content(text):
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


def read_clippings_file():
    """
    读入 My Clippings.txt 文件为列表
    """
    srcFile = open('My Clippings.txt', 'r', encoding='utf-8')
    pieces = srcFile.read().replace(r'\ufeff', '').split("==========\n")
    # 最后一行是"==========\n"，因而 pieces[-1] 为空
    del pieces[-1]

    return pieces


def parse(pieces):
    """
    解析各段落
    """
    books = {}
    for paragraph in pieces:
        title_line, pos_line, _, content_block = paragraph.split('\n', 3)
        title, author = extract_title(title_line)
        pos = extract_position(pos_line)
        content = extract_content(content_block)

        if len(content) > MIN_CONTENT_LENGTH:
            if title not in books:
                books[title] = book(title, author, pos, content)
            else:
                books[title].add(pos, content)
    return books


def export_txt(books):
    """
    将 Kindle 摘录内容输出为 txt 文件
    """

    for book in books.values():
        title = book.name
        print("Generating ...", book.name)

        # 检查 output 文件夹是否存在
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        # 为每本书创建目录
        if os.path.exists(OUTPUT_DIR + os.path.sep + title):
            shutil.rmtree(OUTPUT_DIR + os.path.sep + title)
            os.makedirs(OUTPUT_DIR + os.path.sep + title)
        else:
            os.makedirs(OUTPUT_DIR + os.path.sep + title)

        # 每本书一个文件，输入摘录内容
        with open(OUTPUT_DIR + os.path.sep + title + os.path.sep + title + '.txt', 'w', encoding='utf-8') as file:
            for content_info in book.contents:
                file.write(content_info['content'] + '\n\n')
    print("Done.")


def main():
    books = parse(read_clippings_file())

    export_txt(books)


if __name__ == '__main__':
    main()
