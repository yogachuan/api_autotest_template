from common.rest_client import RestClient
from common.logger import logger


class CustomerApi(RestClient):
    def __init__(self, session):
        super().__init__(session)

    def add_customer_success(self, payload):
        res = self.post('/customer/add', payload=payload, headers=RestClient.header)
        logger.info(f'用户登录 ==>> 返回结果为:{res.text}')
        return res
