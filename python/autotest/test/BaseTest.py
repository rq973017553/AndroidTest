#! /usr/bin/env python
# _*_coding:utf-8_*_
import os
from abc import ABCMeta, abstractmethod
from shell.ShellUtils import ShellUtils
from beans.DeviceInfo import DeviceInfo
from utils.AutoTestUtils import AutoTestUtils


class BaseTest(object):
    """
    抽象类
    对于测试工作的公共代码的抽取
    """
    __metaclass__ = ABCMeta

    def __init__(self, serial_num, module_info, test_info, apk_info):
        self.device_dir = ""
        self.serial_num = serial_num
        self.module_info = module_info
        self.test_info = test_info
        self.apk_info = apk_info
        self.device_info = DeviceInfo()
        self.shell_utils = ShellUtils()
        self.__test_ready()

    def __test_ready(self):
        """执行测试之前的准备工作"""
        self.__get_device_info()
        """
        组合设备信息
        格式:设备型号_设备上AndroidSDK版本_设备cpu类型
        """
        device = (self.device_info.model+'_'+self.device_info.sdk+'_'+self.device_info.cpu).replace(' ', '-')
        print device
        self.device_dir = AutoTestUtils.create_dir(self.test_info.root_dir, device)
        adb_log_file = os.path.join(self.device_dir, self._get_adb_log_file())
        # 创建测试log和日志信息最终存放目录
        self.test_info.adb_log = AutoTestUtils.create_file(adb_log_file)
        # 清除上次自动化测试结果
        self.shell_utils.shell('rm -rf /sdcard/data/', self.serial_num)
        # 卸载被测试apk和测试apk
        self.shell_utils.adb('uninstall '+self.module_info.package_name, self.serial_num)
        self.shell_utils.adb('uninstall '+self.module_info.test_application_id, self.serial_num)
        # 安装被测试apk和测试apk
        self.shell_utils.adb('install '+self.apk_info.test_apk_path, self.serial_num)
        self.shell_utils.adb('install '+self.apk_info.target_apk_path, self.serial_num)

    def _get_adb_log_file(self):
        """
        组合输出日志log
        Android自动化测试项目名_开始测试时间_.log
        """
        return self.module_info.module_name + "_" + self.test_info.start_time + ".log"

    def __get_device_info(self):
        """通过adb shell命令获取设备相关信息"""
        my_shell = self.shell_utils
        manufacturer = self.__get_command_result(my_shell.shell('getprop ro.product.manufacturer',
                                                                self.serial_num, result=True))
        model = self.__get_command_result(my_shell.shell('getprop ro.product.model',
                                                         self.serial_num, result=True))
        if (manufacturer is None or manufacturer == '') and (model is None or model == ''):
            self.device_info.model = self.serial_num
        elif manufacturer is None or manufacturer == '':
            self.device_info.model = model
        else:
            self.device_info.model = manufacturer + "_" + model
        self.device_info.cpu = self.__get_command_result(
            my_shell.shell('getprop ro.product.cpu.abi', self.serial_num, result=True))
        self.device_info.sdk = self.__get_command_result(
            my_shell.shell('getprop ro.build.version.release', self.serial_num, result=True))

    @staticmethod
    def __get_command_result(process):
        result_line = ''
        for line in process.stdout.readlines():
            result_line = result_line+line
        return result_line.strip()

    @abstractmethod
    def exe_auto_test(self):
        pass
