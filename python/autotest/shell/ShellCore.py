#!/usr/bin/env python
# _*_coding:utf-8_*_
from BaseShell import BassShell
import subprocess
import os

# shell("su -c 'svc wifi disable'") 关闭网络


class ShellCore(BassShell):

    def __init__(self, shell_log_path=""):
        self.shell_log_path = shell_log_path
        super(ShellCore, self).__init__()

    def adb(self, cmd, serial_num="", cmd_print=True, result=False):
        devices_serial_num = ShellCore.__devices_select(serial_num)
        adb_data = super(ShellCore, self)._adb(cmd, devices_serial_num, cmd_print)
        if not result:
            self.__collect_shell_log(adb_data)
        else:
            return adb_data

    def shell(self, cmd, serial_num="", cmd_print=True, result=False):
        devices_serial_num = ShellCore.__devices_select(serial_num)
        shell_data = super(ShellCore, self)._shell(cmd, devices_serial_num, cmd_print)
        if not result:
            self.__collect_shell_log(shell_data)
        else:
            return shell_data

    @staticmethod
    def __devices_select(serial_num):
        if serial_num == "":
            devices_serial_num = ""
            devices = ShellCore.get_device_list()
            if len(devices) == 1:
                devices_serial_num = devices[0]
            else:
                # 如果有多个手机会弹出UI用于选择
                pass
            return devices_serial_num
        else:
            return serial_num

    @staticmethod
    def get_device_list():
        devices = []
        result = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE).stdout.readlines()
        result.reverse()
        for device_line in result[1:]:
            if "attached" not in device_line.strip():
                device_split_list = device_line.split()
                devices.append(device_split_list[0])
            else:
                break
        return devices

    def __collect_shell_log(self, process):
        if self.shell_log_path == "":
            print process.stdout.read()
        else:
            if os.path.exists(self.shell_log_path) and os.path.isfile(self.shell_log_path):
                with open(self.shell_log_path, 'w') as f:
                    for line in process:
                        f.write(line+"\n")

if __name__ == "__main__":
    data = ShellCore().shell('"cat /system/build.prop | grep product"', result=True)
    print data.stdout.readlines()