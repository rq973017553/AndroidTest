#!/usr/bin/env python
# _*_coding:utf-8_*_


# 被测试Module(Android自动化测试项目)
class ModuleInfo(object):
    def __init__(self):
        # module路径
        self.module_path = ''

        # module名称
        self.module_name = ''

        # 包名
        self.package_name = ''

        # AndroidStudio项目下的applicationId
        self.test_application_id = ''

        # 测试用例列表
        self.module_tests = []