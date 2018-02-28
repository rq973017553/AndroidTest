#!/usr/bin/env python
# _*_coding:utf-8_*_

# 自动化测试脚本
import sys
from core.ShellDispatchers import ShellDispatchers


def sys_cmd_check():
    cmd_len = len(sys.argv)
    if cmd_len < 3:
        print ('No action specified')
        sys.exit()

if __name__ == "__main__":
    sys_cmd_check()
    ShellDispatchers().dispatch()
