#!/usr/bin/env python
# _*_coding:utf-8_*_
import ttk
import Tkinter

"""
UI相关
测试完毕后的展示页面
后续开发
"""

# http://blog.sina.com.cn/s/blog_9f4f5ca30101omez.html
# http://blog.csdn.net/rgsongzh/article/details/37912177


class DeviceList(object):

    def __init__(self, device_id_list, width=300, height=240):
        self.root = Tkinter.Tk()
        self.__set_window_size__(width, height)
        self.device_id_list = device_id_list
        self.device_id = device_id_list[0]
        self.combo_box = ttk.Combobox(self.root, values=device_id_list)
        # self.button = ttk.Button(self.root, text="确定")
        # self.__create_button__()
        self.__create_combo_box__()

    def set_title(self, title):
        self.root.title(title)

    def __create_combo_box__(self):
        self.combo_box.current(0)
        self.combo_box.pack(expand=Tkinter.YES)
        self.combo_box.bind("<<ComboboxSelected>>", self.select)

    # def __create_button__(self):
    #     self.button.pack(side=Tkinter.BOTTOM)

    def show_window(self):
        print "show_window"
        self.root.mainloop()

    def __set_window_size__(self, width, height):
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(size)

    def set_on_click_listener(self, method):
        print "=====================set_on_click_listener========================"
        # button = ttk.Button(self.root, text="确定", command=self.ok)
        button = ttk.Button(self.root, text="确定", command=self.binder(method))
        # button = ttk.Button(self.root, text="确定", command=lambda fun=method, parameter=self.device_id: fun(parameter))
        button.pack(side=Tkinter.BOTTOM)
        # self.button.bind("<Button>", self.binder(method))

    def ok(self):
        print "ok!!!!"+str(self.device_id)

    def select(self, event):
        self.device_id = self.combo_box.selection_get()
        print "select::"+str(self.device_id)

    def binder(self, function):
        print "__binder__"+str(self.device_id)
        return lambda fun=function, parameter=self.device_id: fun(parameter)
