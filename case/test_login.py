import os.path

from lib.loginApi import LoginApi
from common.read_data import read_data
from common.logger import logger
from common.getSession import GetSessionID
import unittest
from ddt import ddt, data, unpack


@ddt
class LoginTest(unittest.TestCase):
    """登录类测试"""
    base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    case_data = read_data.load_excel(os.path.join(base_path, 'data', 'login_nor.xlsx'))
    logger.info(f'登录类测试用例数据为{case_data}')

    @classmethod
    def setUpClass(cls) -> None:
        logger.info("class setup content")

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info("Class teardown content")

    def setUp(self) -> None:
        logger.info("function setup content")
        self.ses = GetSessionID.sessionMethod(case='login')
        self.login_api = LoginApi(self.ses)

    def tearDown(self) -> None:
        logger.info("function teardown content")

    @data(*case_data)
    @unpack
    def test_login_success(self, case, desc, usr, pwd, code, ass):
        logger.info(f'用例名{case},用例描述{desc}')
        res = self.login_api.login_user(usr, pwd, code)
        # res_json = res.json()
        print(f"res:{res.text}")
        self.assertIn(ass, res.text)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(LoginTest())
    runner = unittest.TextTestRunner
    test_result = runner.run(suite)