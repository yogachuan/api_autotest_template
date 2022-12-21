import os.path
from lib.customerApi import CustomerApi
from common.read_data import read_data
from common.logger import logger
from common.getSession import GetSessionID
import unittest
from ddt import ddt, data, unpack
from common.database_operate import db


@ddt
class CustomerAddTest(unittest.TestCase):
    """新增会员测试类"""
    base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    file_data = read_data.load_excel(os.path.join(base_path, 'data', 'customer_add_nor.xlsx'))
    logger.info(f'新增会员成功的用例数据为{file_data}')

    @classmethod
    def setUpClass(cls) -> None:
        logger.info("class setup content")

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info("Class teardown content")

    def setUp(self) -> None:
        logger.info("function setup content")
        self.ses = GetSessionID.sessionMethod()
        self.customer_api = CustomerApi(self.ses)

    def tearDown(self) -> None:
        logger.info("function teardown content")
        for i in range(len(self.file_data)):
            # print(self.file_data[i][2])
            db.execute_db(f"DELETE FROM customer WHERE customername = '{self.file_data[i][2]}'")

    @data(*file_data)
    @unpack
    def test_customer_add_success(self, case, desc, name, phone, sex, birthday, creditkids, creditcloth, ass):
        logger.info(f'用例名{case},用例描述{desc}')
        res = self.customer_api.add_customer_success(name, phone, sex, birthday, creditkids, creditcloth)
        print(res)
        self.assertIn(ass, res.text)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(CustomerAddTest())
    runner = unittest.TextTestRunner()
    test_result = runner.run(suite)
