# -*- coding: utf-8 -*-
# By: Mei
import unittest
import os
import HTMLTestRunner
import time


cur_path = os.path.dirname(os.path.realpath(__file__))
case_path = os.path.join(cur_path, "case")        # 测试用例的路径
report_path = os.path.join(cur_path, "report")  # 报告存放路径

if __name__ == "__main__":
    discover = unittest.defaultTestLoader.discover(case_path,"test*.py")
    print(discover)
    filename=time.strftime("%Y-%m-%d-%H-%M")
    run = HTMLTestRunner.HTMLTestRunner(title="带饼图报告",
                                            description="测试用例参考",
                                            # stream=open(report_path+"\\2018-3-16.html", "wb"),
                                            stream=open(report_path+"\\"+filename+"测试报告.html", "wb"),
                                            retry=1)

    run.run(discover)