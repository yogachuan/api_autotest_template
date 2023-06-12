from XTestRunner import HTMLTestRunner
import unittest
import platform
import os
import time
import sys
from common.logger import logger


# 将项目根目录加到系统路径中，避免jenkins执行python时，common模块识别不出的问题
rootpath = os.path.dirname(os.path.realpath(__file__))
syspath = sys.path

print("syspath is:{}".format(syspath))
sys.path.append(rootpath)
print("syspath is:{}".format(sys.path))


class RunCase(object):
    # 当前时间
    now_date = time.strftime('%Y%m%d', time.localtime(time.time()))
    now_time = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
    # 构造HtmlTestRunner 测试报告路径
    root_path = os.path.dirname(os.path.realpath(__file__))
    result_date_dir = os.path.join(root_path, f'result', now_date)
    if not os.path.exists(result_date_dir):
        os.makedirs(result_date_dir)
    report_file_path = os.path.join(result_date_dir, "ui_auto_result_{}.html".format(now_time))

    #执行用例函数
    def run_case(self):
        # 运行测试用例并生成html测试报告
        with open(self.report_file_path, 'wb') as fp:
            try:
                logger.info("RunCase执行用例--开始")
                suite = unittest.TestSuite()
                # 查找run.py文件同一级目录（case）下的所有名称为test_*.py下的所有测试用例
                tests = unittest.defaultTestLoader.discover('./case', pattern='test_*.py')
                suite.addTest(tests)
                runner = HTMLTestRunner(stream=fp,
                                        title=u'自动化测试报告',
                                        description=u'运行环境：{}'.format(platform.platform()),
                                        verbosity=2,
                                        language='zh-CN',
                                        tester='yogachuan'
                                        )
                runner.run(suite)
                logger.info("RunCase执行用例--结束")
            except Exception as e:
                logger.error("RunCase执行用例，生成报告失败：{}".format(e))


if __name__ == '__main__':
    test = RunCase()  # 创建对象
    test.run_case()  # 调用测试用例执行函数