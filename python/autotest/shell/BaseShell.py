#!/usr/bin/env python
# _*_coding:utf-8_*_
import platform
import os
import subprocess
from abc import ABCMeta, abstractmethod

"""
adb:
adb.exe -s HC46AWW01937 version

shell:
adb.exe -s HC46AWW01937 shell adb version
"""


class BassShell(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        # 判断是否设置环境变量ANDROID_HOME
        self.system = platform.system()
        if "ANDROID_HOME" in os.environ:
            if self.system == "Windows":
                self._command = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb.exe")
            else:
                self._command = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb")
        else:
            raise EnvironmentError(
                "Adb not found in $ANDROID_HOME path: %s." % os.environ["ANDROID_HOME"])

    # adb命令
    def _adb(self, args, serial_num, cmd_print=True):
        cmd = "%s -s %s %s" % (self._command, serial_num, str(args))
        if cmd_print:
            print "adb::"+cmd
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # adb shell命令
    def _shell(self, args, serial_num, cmd_print=True):
        cmd = "%s -s %s shell %s" % (self._command, serial_num, str(args))
        if cmd_print:
            print "shell::"+cmd
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    @abstractmethod
    def adb(self, args, serial_num):
        pass

    @abstractmethod
    def shell(self, args, serial_num):
        pass

if __name__ == "__main__":
    pass
