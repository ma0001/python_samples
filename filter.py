#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# コマンドライン引数でファイルを指定しなければ、標準入力から1行ずつ読み込む。

import fileinput
import re

# 行番号を付けてマッチした内容を出力する
for line in fileinput.input():
    match = re.search(r'(\d+)', line)
    if match:
        print(f"{fileinput.filename()}({fileinput.filelineno()}) : {match.group(1)}")



    
