#! /usr/bin/env python
# _*_coding:utf-8_*_
import os
from core.NoDaemonProcess import NoDaemonProcess
from utils.AutoTestUtils import AutoTestUtils
from test.BaseTest import BaseTest

junit_runner = 'com.avl.automationtest.AutoAndroidJUnitRunner'

# 过滤掉该字段
log_filter_tag = "</testsuite></testsuites>" \
                 "<?xml version='1.0' encoding='utf-8' standalone='yes' ?>" \
                 "<testsuites><testsuite>"


# 方法，开启进程(取消守护的进程)
def process_start(target, args):
    print args
    process = NoDaemonProcess(target=target, args=args)
    process.start()
    return process


class ExeAutoTest(BaseTest):
    """
    功能测试，所有测试用例只执行一遍
    关键命令如下：
    am instrument -w -e class
    pm clear命令，清除数据
    """
    def __init__(self, serial_num, module_info, test_info, apk_info):
        super(ExeAutoTest, self).__init__(serial_num, module_info, test_info, apk_info)

    def exe_auto_test(self):
        # adb logcat进程，用于输出测试中打印的log
        process = process_start(os.system, ("adb -s "+self.serial_num+" logcat > " + self.test_info.adb_log,))
        package_name = self.module_info.package_name
        test_package_name = self.module_info.test_application_id
        """
        通过在ShellDispatchers类中获得的所有测试case。
        按照顺序执行测试case
        """
        for cmd in self.module_info.module_tests:
            self.shell_utils.shell("am instrument -w -e class " + cmd + " " +
                                   test_package_name + "/" + junit_runner, self.serial_num)
            self.shell_utils.shell("pm clear "+package_name, self.serial_num)
        process.terminate()
        path = os.path.split(self.test_info.adb_log)[0]
        temp_log = os.path.join(path, "temp.xml")
        # pull出自动化测试完成的测试log
        self.shell_utils.adb("pull /sdcard/data/"+package_name+"/log.xml "+temp_log, self.serial_num)
        # 删除已经pull出的测试log
        self.shell_utils.shell("rm -rf /sdcard/data/"+package_name+"/log.xml", self.serial_num)
        # 卸载被测试apk
        self.shell_utils.adb('uninstall ' + package_name, self.serial_num)
        # 卸载测试apk
        self.shell_utils.adb('uninstall ' + test_package_name, self.serial_num)
        AutoTestUtils.handle_test_log(path, self.module_info.module_name, self.test_info.start_time)
        self.shell_utils.shell("am force-stop " + package_name)

if __name__ == "__main__":
    pass
