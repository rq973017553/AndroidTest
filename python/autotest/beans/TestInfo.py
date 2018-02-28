#!/usr/bin/env python
# _*_coding:utf-8_*_


# 测试log
class TestInfo(object):
    def __init__(self):
        # adb log输出
        self.adb_log = ''

        # 测试报告
        self.report_log = ''

        # 测试的时间
        self.start_time = ''

        # 测试log存放的根目录
        self.root_dir = ''