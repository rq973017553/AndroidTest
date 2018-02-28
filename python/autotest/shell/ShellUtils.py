#!/usr/bin/env python
# _*_coding:utf-8_*_
from shell.ShellCore import ShellCore


class ShellUtils(object):
    def __init__(self, shell_log_path=""):
        self.__shell_core = ShellCore(shell_log_path)

    def adb(self, cmd, serial_num="", cmd_print=True, result=False):
        return self.__shell_core.adb(cmd, serial_num, cmd_print, result)

    def shell(self, cmd, serial_num="", cmd_print=True, result=False):
        return self.__shell_core.shell(cmd, serial_num, cmd_print, result)

    def batch_adb(self):
        pass

    def batch_shell(self):
        pass

    @staticmethod
    def get_device_list():
        return ShellCore.get_device_list()