#! /usr/bin/env python
# _*_coding:utf-8_*_
import os
import sys
from NoDaemonPool import NoDaemonPool
from beans.ModuleInfo import ModuleInfo
from beans.TestInfo import TestInfo
from beans.APKInfo import APKInfo
from shell.ShellUtils import ShellUtils
from core.ShellExecute import ShellExecute
from utils.AutoTestUtils import AutoTestUtils

# 进程池中进程数量
MAX_PROCESS_NUM = 3


def process_start(serial_num, module_info, test_info, apk_info):
    ShellExecute(serial_num, module_info, test_info, apk_info).execute()


class ShellDispatchers(object):
    """
    对整个测试系统开始之前做准备工作
    """
    def __init__(self, processes=MAX_PROCESS_NUM):
        # 创建ModuleInfo类
        self.module_info = ModuleInfo()
        # 创建TestInfo类
        self.test_info = TestInfo()
        # 创建APKInfo类
        self.apk_info = APKInfo()
        # 创建自定义的线程池
        self.pool = NoDaemonPool(processes)

    def dispatch(self):
        # 系统运行前的准备工作
        self.__ready()
        # 执行gradle相关命令，编译apk
        self.__exe_gradle()
        # 获取当前连接到主机的所有android设备
        device_list = ShellUtils.get_device_list()
        # 针对列表中的每个android设备运行测试用例
        for device in device_list:
            # 进程池技术
            self.pool.apply_async(process_start, (device, self.module_info, self.test_info, self.apk_info))
        self.pool.close()
        self.pool.join()
        os.system("adb kill-server")

    def __ready(self):
        # 初始化被测试项目的信息
        self.__my_module()
        # 创建测试log的存放目录
        self.__my_test_log()

    def __my_test_log(self):
        """
        创建测试log根目录
        目录格式:auto_test/测试时间/
        """
        path = AutoTestUtils.create_dir(os.path.dirname(os.path.realpath(sys.argv[0])), 'auto_test')
        self.test_info.start_time = AutoTestUtils.get_current_time()
        self.test_info.root_dir = AutoTestUtils.create_dir(path, self.test_info.start_time)

    def __my_module(self):
        """
        通过传入的Android测试项目路径，获取该项目的信息
        """
        module_path = sys.argv[-1]
        if os.path.exists(module_path):
            if os.path.isdir(module_path):
                # 获得Android测试项目路径
                self.module_info.module_path = module_path
                # 获得Android测试项目项目名
                self.module_info.module_name = os.path.basename(module_path)
                # 获得Android测试项目的所有testcase
                self.module_info.module_tests = AutoTestUtils.get_all_test(module_path)
                # 获得Android测试项目的包名
                self.module_info.package_name = AutoTestUtils.get_package_name(module_path)
                """
                获得Android测试项目的testApplicationId
                可能有的被测试的项目的包名存在非法命名(测试apk将无法编译通过)，
                这个时候可以设置testApplicationId。
                """
                test_application_id = AutoTestUtils.get_test_application_id(module_path)
                if test_application_id == "":
                    """
                    如果testApplicationId不存在，
                    那么测试apk的包名将是
                    "被测试项目包名"+".test"
                    """
                    test_application_id = self.module_info.package_name+".test"
                self.module_info.test_application_id = test_application_id
                print 'package_name::'+self.module_info.package_name
                print 'test_application_id::'+self.module_info.test_application_id
            else:
                print ('No This Module!')
                sys.exit()
        else:
            print ('No This Module!')
            sys.exit()

    def __exe_gradle(self):
        """
        使用gradle命令构建测试apk和被测试apk
        """
        os.system('adb start-server')
        os.system("adb logcat -c")
        os.chdir(self.module_info.module_path)
        os.system('gradle clean')
        # 构建被测试apk
        os.system('gradle assembleDebug')
        # 构建测试apk
        os.system('gradle assembleDebugAndroidTest')
        # 构建的apk存放地址
        path = os.path.join(self.module_info.module_path, 'build/outputs/apk')
        self.apk_info.test_apk_path = os.path.join(path,
                                                   self.module_info.module_name+'-debug-androidTest-unaligned.apk')
        self.apk_info.target_apk_path = os.path.join(path, self.module_info.module_name+'-debug-unaligned.apk')


if __name__ == "__main__":
    pass
