#!/usr/bin/env python
# _*_coding:utf-8_*_


# 生成的apk
class APKInfo(object):
    def __init__(self):
        # 生成apk存放路径的根路径
        self.root_dir = ''
        # 测试apk存放路径(测试apk指的是通过java test case生成的)
        self.test_apk_path = ''
        # 被测试的目标apk
        self.target_apk_path = ''
