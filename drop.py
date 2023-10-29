#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ファイルをドラッグ&ドロップしてファイルの内容を表示するアプリ
# pip install tkinterdnd2-universal でインストールする必要がある

import sys
import tkinter
import os.path
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog

# 入力中のファイルパスと現在の補完名をとり、次の補完名候補を返す
def complete_next(file_path, current_completion):
    # 最後の/を削除
    file_path = file_path.rstrip("/")
    current_completion = current_completion.rstrip("/")
    file_path = os.path.expanduser(file_path)
    current_completion = os.path.expanduser(current_completion)
    # ディレクトリーと候補の先頭文字列を取り出す
    if os.path.isdir(file_path):
        dir_path = file_path
        start_name = ""
    else:
        dir_path = os.path.dirname(file_path)
        start_name = os.path.basename(file_path)

#    print(f"dir_path={dir_path}, start_name={start_name}")

    # ディレクトリでない場合は、何もしない
    if not os.path.isdir(dir_path):
        return current_completion

    # そのディレクトリ内のstart_nameで始まるファイル名を取得する
    files = os.listdir(dir_path)
    files = [f for f in files if os.path.basename(f).startswith(start_name)]
    files = [os.path.join(dir_path, f) for f in files]
    
    # ファイル名を辞書順にソートする
    files.sort()

    # 補完候補がないなら、何もしない
    if len(files) == 0:
        return current_completion

    try:
        next_index = files.index(current_completion) + 1
        if next_index >= len(files):
            next_index = 0
    except ValueError:
        next_index = 0

    return files[next_index]
    

# ファイルのドラッグ&ドロップを受け取るファイル選択ダイアログ、ファイル選択時にコールバックする
class FileSelectorFrame(tkinter.Frame):
    def __init__(self, master=None, callback=None):
        super().__init__(master)
        self.callback = callback
        self.__inputpath = ''   # ファイルパス補完のベースとなる文字列
        self.__initialtext = 'you can drop file here'
        self.__create_widgets()

    def __create_widgets(self):
        self._button = tkinter.Button(self, text="File...", command=self.__select_file)
        self._button.pack(side="right")

        self._entry = tkinter.Entry(self)
        self._entry.pack(side="right", fill="both", expand=True)
        self._entry.insert(0, self.__initialtext)
        self._entry.drop_target_register(DND_FILES)
        self._entry.dnd_bind("<<Drop>>", self.__drop)
        self._entry.bind("<Button-1>", self.__button1)
        self._entry.bind("<Return>", self.__return)
        self._entry.bind("<Tab>", self.__tab)
        self._entry.bind("<Key>", self.__key)

    def __select_file(self):
        # ファイル選択ダイアログを表示する、_entryにあるファイルパスを初期値とする
        file_path = self._entry.get()
        if not os.path.exists(file_path):
            file_path = "~"
        file_path = filedialog.askopenfilename(initialdir = os.path.dirname(file_path),
                                               initialfile = os.path.basename(file_path))
        if file_path:
            self.set_file_path(file_path)
            if self.callback:
                self.callback(self)

    def __button1(self, event):
        if self.__initialtext:
            self._entry.delete(0, "end")
            self.__initialtext = None
                    
    def __return(self, event):
        if not os.path.isfile(self.get_file_path()):
            self.__select_file()
        else:
            if self.callback:
                self.callback(self)

    def __tab(self, event):
        file_path = self.get_file_path()
        if not self.__inputpath:
            self.__inputpath = file_path
        file_path = complete_next(self.__inputpath, file_path)
        if file_path:
            self.set_file_path(file_path)
        # フォーカスを移動させない
        return "break"

    def __key(self, event):
        # 何か入力されたら__inputpathをクリアする
        self.__inputpath = None
            
    def __drop(self, event):
        self.set_file_path(event.data)
        if self.callback:
            self.callback(self)

    def get_file_path(self):
        return self._entry.get()

    def set_file_path(self, file_path):
        self._entry.delete(0, "end")
        self._entry.insert(0, file_path)


class Myapp(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.fileselector = FileSelectorFrame(self, self.__fileselector_callback)
        self.fileselector.pack(side="top", fill="x")
        self.text = tkinter.Text(self)
        self.text.pack(fill="both", expand=True)

    def __fileselector_callback(self, fileselector):
        # ファイルが選択されたらファイルの内容を表示する
        file_path = fileselector.get_file_path()
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                self.text.delete("1.0", "end")
                self.text.insert("end", f.read())


root = TkinterDnD.Tk()
app = Myapp(master=root)
app.mainloop()

