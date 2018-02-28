#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
UI相关
测试完毕后的展示页面
后续开发
"""

import Tkinter
import ttk


class TestEndRemind(object):
    def __init__(self, width=300, height=240):
        self.root = Tkinter.Tk()
        # self.__set_window_size__(width, height)
        self.frame = ttk.Frame(self.root, width, height).pack()
        self.button = ttk.Button(self.root, text="确定")

    def __set_window_size__(self, width, height):
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(size)

    def show_window(self):
        self.root.mainloop()