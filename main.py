import HTMLTestRunnerNew
import unittest
from testcases import test_api_case_v1
from common import dir_config
import time


s = unittest.TestSuite()
ul = unittest.TestLoader()
s.addTests(ul.loadTestsFromModule(test_api_case_v1))
curTime = time.strftime("%Y-%m-%d %H%M", time.localtime())
fp = open(dir_config.report_dir + '/API_autoTest_{0}.html'.format(curTime), 'wb')
runner = HTMLTestRunnerNew.HTMLTestRunner(
            stream=fp,
            title='gpet接口测试报告',
            description='gpet接口测试报告',
            tester="zhihui"
            )
runner.run(s)
