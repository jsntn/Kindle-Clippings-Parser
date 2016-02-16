# -*- coding: utf-8 -*-
from __future__ import print_function
import re


def handleContent(text):
    temp = text.strip()
    if temp.startswith(('，', '：', '。')):
        print('问题段开始:', temp)
        temp = temp[1:]
        print('问题段结束:', temp)
    if not temp.endswith('。'):
        if temp.endswith(('？', '！', '”','；')):
            pass
        elif temp.endswith(('，', '：')):
            temp = temp[:-1] + '。'
        else:
            temp = temp + '。'
    return temp + '\n'


ifile = open('duokan.txt', 'r', encoding='gbk')
ofile = open('duokan_Markdown.md', 'w', encoding='utf-8')

ptime = re.compile(r'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d\n')
phead = re.compile(r'\s([^ ].*)\n')
first = True

for line in ifile.readlines()[:-2]:
    if first:
        first = False
        line = '# ' + line
        ofile.write(line + '\n')
        # ofile.write('@(读书笔记)[Kindle|未整理|阅读]\n')
        # ofile.write('\n[TOC]\n')
        continue
    if line.strip():

        if ptime.match(line):
            line = ptime.sub('', line)
        elif phead.match(line):
            print(line)
            line = phead.sub(r'## \1', line)
            ofile.write('\n')
        else:
            line = handleContent(line)

        ofile.write(line + '\n')

ofile.close()
