# _*_coding:utf-8_*_

import os
import time
import multiprocessing
from multiprocessing import Process
from shell.ShellUtils import ShellUtils

BASE_CMD = 'dumpsys meminfo '
# 每GET_MEMORY_MAX_TIME秒刷新一次
DEFAULT_GET_MEMORY_MAX_TIME = 30.0
# 找不到你输入的包名的进程
NO_PROCESS_FOUND = 'No process found'


class TestMemory(Process):
    """
    测试内存的进程类，利用dumpsys meminfo命令
    该类直接继承Process类
    """
    def __init__(self):
        super(TestMemory, self).__init__()
        self.shell = ShellUtils()
        self.cmd_print = True
        self.save_path = ''
        self.package_name = ''
        self.serial_num = ''
        self.running = multiprocessing.Value('b', False)
        self.interval_time = DEFAULT_GET_MEMORY_MAX_TIME

    def run(self):
        test_memory_result_path = os.path.join(self.save_path, 'test_memory_result.log')
        with open(test_memory_result_path, 'w') as memory_result_file:
            head = '%s %s %s %s %s' % ("time", "java_heap_total", 'java_heap_alloc',
                                       "native_heap_total", "native_heap_alloc")
            memory_result_file.write(head+'\n')
            while True:
                if not self.running.value:
                    print "Stop Capture Memory Process!"
                    break
                time_result = self.shell.shell("date +%d::%H:%M:%S", serial_num=self.serial_num,
                                               cmd_print=self.cmd_print, result=True)
                memory_result = self.shell.shell(BASE_CMD+self.package_name, serial_num=self.serial_num,
                                               cmd_print=self.cmd_print, result=True)
                memory_data_list = memory_result.stdout.readlines()
                current_time = time_result.stdout.readlines()[0].strip()
                if len(memory_data_list) <= 0 or (NO_PROCESS_FOUND in memory_data_list[0].strip()):
                    time.sleep(2)
                    if self.cmd_print:
                        print self.package_name+" not found!"
                    continue
                # 保证能够读取到内存数据
                if len(memory_data_list) < 8:
                    continue
                # 去除空格
                native_heap_list = ' '.join(memory_data_list[7].strip().split()).split()
                java_heap_list = ' '.join(memory_data_list[8].strip().split()).split()
                java_heap_total = java_heap_list[6]
                java_heap_alloc = java_heap_list[7]
                native_heap_total = native_heap_list[6]
                native_heap_alloc = native_heap_list[7]
                line = '%s %s %s %s %s' % (current_time, java_heap_total,
                                           java_heap_alloc, native_heap_total,
                                           native_heap_alloc)
                memory_result_file.write(line+'\n')
                memory_result_file.flush()
                time.sleep(self.interval_time)

    def start_test(self, package_name, interval_time=DEFAULT_GET_MEMORY_MAX_TIME,
                   save_path=os.getcwd(), cmd_print=True, serial_num=""):
        """
        通过该方法开启获取内存数据进程
        :param package_name: 被测试的包名
        :param interval_time: 每隔interval_time秒获取一次内存数据
        :param save_path: 获取的内存数据存放文件路径
        :param cmd_print: 是否打印命令
        :param serial_num: android设备的serial_num
        """
        self.cmd_print = cmd_print
        self.save_path = save_path
        self.interval_time = interval_time
        self.running.value = True
        self.package_name = package_name
        self.serial_num = serial_num
        super(TestMemory, self).start()

    def stop(self):
        """
        stop方法，终止获取内存信息进程
        """
        self.running.value = False

if __name__ == "__main__":
    pass

