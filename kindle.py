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


def handleBookName(text):
    name = ''
    author = ''
    ls = text.split(' ', 1)
    pname = re.compile('[\ufeff](.*)')
    pSpecialName = re.compile('[:](.*?)[(]')
    pauthor = re.compile(r'\((.*?)\)')

    specialNameRes = pSpecialName.search(ls[0])
    if not specialNameRes:
        nameres = pname.search(ls[0])
    else:
        nameres = specialNameRes
    authorres = pauthor.search(ls[-1])
    name = nameres.group(1)
    author = authorres.group(1)
    return name.strip(), author.strip()


def handlePos(text):
    pattern = re.compile('#(\d*)')
    res = pattern.search(text)
    return res.group(1)


def handleContent(text):
    temp = text.strip()
    if temp.startswith(('，', '：')):
        temp = temp[1:]
    if not temp.endswith('。'):
        if temp.endswith(('？', '！', '”')):
            pass
        elif temp.endswith(('，', '：')):
            temp = temp[:-1] + '。'
        else:
            temp = temp + '。'
    pattern = re.compile('(\s+)')
    temp = pattern.sub('\n', temp)

    return temp

bookList = {}
srcFile = open(r"My Clippings.txt", 'r', encoding='utf-8')
allPieces = srcFile.read().split("==========\n")
del allPieces[-1]

for paragraph in allPieces:
    ls = paragraph.split('\n', 3)
    bookname = ''
    author = ''
    pos = ''
    content = ''
    bookname, author = handleBookName(ls[0].strip())
    pos = handlePos(ls[1].strip())
    content = handleContent(ls[3])
    if len(content) > 3:
        if not bookname in bookList.keys():
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
