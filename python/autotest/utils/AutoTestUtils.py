#!/usr/bin/env python
# _*_coding:utf-8_*_
import os
import datetime
import platform
import signal
from shell.ShellUtils import ShellUtils

build_gradle = 'build.gradle'
applicationId = 'applicationId'
test_application_id = 'testApplicationId'
android_manifest = 'AndroidManifest.xml'
package = 'package'
filter_tag = 'com.avl.automationtest'
log_filter_tag = "</testsuite></testsuites>" \
                 "<?xml version='1.0' encoding='utf-8' standalone='yes' ?>" \
                 "<testsuites><testsuite>"


class AutoTestUtils(object):

    @staticmethod
    def get_package_name(module_path):
        """ 通过Module中的build.gradle文件的applicationId属性获得包名"""
        manifest_path = os.path.join(module_path, android_manifest)
        path = os.path.join(module_path, build_gradle)
        with open(path, 'r') as build_file:
            for build_line in build_file:
                # 判断该行是否存在"applicationId"
                if applicationId in build_line:
                    return build_line.split('"')[1]
        with open(manifest_path, 'r') as manifest_file:
            for manifest_line in manifest_file:
                # 判断该行是否存在"package"
                if package in manifest_line:
                    return manifest_line.strip().split('"')[1]
        print "No Found PackageName"

    @staticmethod
    def get_test_application_id(module_path):
        """ 通过Module中的build.gradle文件的testApplicationId属性获得包名"""
        path = os.path.join(module_path, build_gradle)
        with open(path, 'r') as build_file:
            for build_line in build_file:
                # 判断该行是否存在"applicationId"
                if test_application_id in build_line:
                    return build_line.split('"')[1]
        print "No Found testApplicationId"
        return ""

    @staticmethod
    def get_all_test(module_path):
        """ 获得Module/src/androidTest/java下的所有测试case"""
        tests = []
        all_test_path = os.path.join(module_path, "src", "androidTest", "java")
        for root, dirs, files in os.walk(all_test_path):
            for f in files:
                test_path = os.path.join(root, f)
                suffix_name = os.path.splitext(test_path)[1]
                if suffix_name == '.java':
                    test = test_path.split("java" + os.path.sep)[1].split(".java")[0].replace(os.path.sep, ".")
                    if filter_tag not in test:
                        tests.append(test)
        return tests

    @staticmethod
    def create_dir(root, path):
        """通用创建dir方法"""
        my_dir = os.path.join(root, path)
        if not os.path.exists(my_dir):
            os.mkdir(my_dir)
        return my_dir

    @staticmethod
    def create_file(file_path):
        """通用创建文件方法"""
        open(file_path, 'w').close()
        return file_path

    @staticmethod
    def get_current_time():
        """
        获取当前时间
        格式是:年_月_日_时_分_秒
        :return: 获取到当前时间
        """
        return datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    # 处理最后输出的日志
    @staticmethod
    def handle_test_log(root, module_name, time):
        """ 从手机得到的测试报告temp文件，去除多余的xml字段，重新写入文件中"""
        temp = os.path.join(root, "temp.xml")
        test_log = os.path.join(root, module_name + "_" + time + ".xml")
        if os.path.exists(temp):
            with open(temp, "r") as temp_file:
                with open(test_log, "w") as test_file:
                    for line in temp_file:
                        if log_filter_tag not in line:
                            test_file.write(line)
            os.remove(temp)
        else:
            print ("temp.xml is not exists!")

    @staticmethod
    def kill_process(pid):
        """
        杀死指定pid的进程
        :param pid: 进程PID
        """
        system = platform.system()
        if 'Windows' in system:
            # windows平台下
            os.system("taskkill /F /T /PID " + str(pid))
        else:
            # 非windows平台，主要是linux平台
            os.kill(pid, signal.SIGILL)

    @staticmethod
    def get_pid(package_name, serial_num=""):
        """获取指定包名的android进程pid"""
        print package_name
        print serial_num
        cmd = '"'+'ps | grep ' + package_name+'"'
        result = ShellUtils().shell(cmd, serial_num=serial_num, result=True)
        line = result.stdout.read()
        print "get_pid::"+line
        pid = line.split()[1]
        return pid

if __name__ == "__main__":
    pass

