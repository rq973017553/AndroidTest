#! /usr/bin/env python
# _*_coding:utf-8_*_
import sys
from test.ExeAutoTest import ExeAutoTest
from test.BatchExeAutoTest import BatchExeAutoTest


class ShellExecute(object):
    """
    通过传入的命令，区分是'-bt'还是'-t'
    '-t'正常执行测试用例，只执行一遍。也就是"功能测试"
    '-bt'该命令是"压力测试"，后面的数字代表执行多少遍
    """
    def __init__(self, serial_num, module_info, test_info, apk_info):
        self.argv = sys.argv
        self.serial_num = serial_num
        self.module_info = module_info
        self.test_info = test_info
        self.apk_info = apk_info

    def execute(self):
        """
        通过命令区分是-bt还是-t
        """
        if self.argv[1].startswith('-'):
            option = self.argv[1][1:]
            if option == 't' or option == 'test':
                test = ExeAutoTest(self.serial_num, self.module_info, self.test_info, self.apk_info)
                test.exe_auto_test()
            elif option == 'bt':
                batch_num = self.argv[2]
                batch_test = BatchExeAutoTest(batch_num, self.serial_num, self.module_info, self.test_info, self.apk_info)
                batch_test.exe_auto_test()

if __name__ == "__main__":
    pass
