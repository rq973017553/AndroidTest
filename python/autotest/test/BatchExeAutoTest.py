#! /usr/bin/env python
# _*_coding:utf-8_*_
import os
import multiprocessing
from core.NoDaemonProcess import NoDaemonProcess
from utils.AutoTestUtils import AutoTestUtils
from test.BaseTest import BaseTest
from utils.Memory import TestMemory

junit_runner = 'com.avl.automationtest.AutoAndroidJUnitRunner'

log_filter_tag = "</testsuite></testsuites>" \
                 "<?xml version='1.0' encoding='utf-8' standalone='yes' ?>" \
                 "<testsuites><testsuite>"

MAX_DEFAULT_INTERVAL_TIME = 20


# 方法，开启进程(取消守护的进程)
def process_start(target, args):
    process = NoDaemonProcess(target=target, args=args)
    process.start()
    return process


# 方法，开启进程(取消守护的进程)
def exe_task(shell, cmd, serial_num, queue):
    process = shell.adb(cmd, serial_num, result=True)
    # 获取进程pid存入到queue中
    queue.put(process.pid)


class BatchExeAutoTest(BaseTest):
    """
    压力测试，通过'-bt'后面的数字控制压力测试的执行的次数
    """
    def __init__(self, batch_num, serial_num, module_info, test_info, apk_info):
        self.batch_num = int(batch_num)
        # 用于进程间的通讯
        self.queue = multiprocessing.Queue(1)
        super(BatchExeAutoTest, self).__init__(serial_num, module_info, test_info, apk_info)

    def exe_auto_test(self):
        os.remove(self.test_info.adb_log)
        package_name = self.module_info.package_name
        test_package_name = self.module_info.test_application_id

        # 初始化和开启获取内存进程
        test_memory = TestMemory()
        test_memory.start_test(package_name, interval_time=MAX_DEFAULT_INTERVAL_TIME, save_path=self.device_dir,
                               cmd_print=False, serial_num=self.serial_num)
        # 压力测试执行次数
        for i in range(self.batch_num):
            self.test_info.start_time = AutoTestUtils.get_current_time()
            self.test_info.adb_log = AutoTestUtils.create_file(os.path.join(self.device_dir, self._get_adb_log_file()))
            process = process_start(exe_task, (self.shell_utils, "logcat > " +
                                               self.test_info.adb_log,
                                               self.serial_num, self.queue))

            self.shell_utils.shell("rm -rf /sdcard/data/" + package_name + "/log.xml", self.serial_num)
            # 执行所有的测试case
            for cmd in self.module_info.module_tests:
                self.shell_utils.shell("am instrument -w -e class " + cmd + " " +
                                       test_package_name + "/" + junit_runner, self.serial_num)
                self.shell_utils.shell("pm clear "+package_name, self.serial_num)
            # 取出queue中的pid
            pid = self.queue.get()
            print "====kill_process==="+str(pid)+"======"
            # 杀死该pid的进程
            AutoTestUtils.kill_process(pid)
            process.terminate()
            process.join()
            root_path = os.path.split(self.test_info.adb_log)[0]
            temp_log = os.path.join(root_path, "temp.xml")
            # pull出自动化测试完成的测试log
            self.shell_utils.adb("pull /sdcard/data/"+package_name+"/log.xml "+temp_log, self.serial_num)
            AutoTestUtils.handle_test_log(root_path, self.module_info.module_name, self.test_info.start_time)
            self.shell_utils.shell("am force-stop "+package_name)
        # 当压力测试结束后，关闭内存数据捕获进程
        test_memory.stop()

if __name__ == "__main__":
    pass
