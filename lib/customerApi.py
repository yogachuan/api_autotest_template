from common.rest_client import RestClient
from common.logger import logger


class CustomerApi(RestClient):
    def __init__(self, session):
        super().__init__(session)
        self.header = {
            'Content-Type': self.api_content_type
        }

    def add_customer_success(self, name, phone, sex, birthday, creditkids, creditcloth):
        payload = {
            'customername': name,
            'customerphone': phone,
            'childsex': sex,
            'childdate': birthday,
            'creditkids': creditkids,
            'creditcloth': creditcloth
        }
        res = self.post('/customer/add', payload=payload, headers=self.header)
        logger.info(f'用户登录 ==>> 返回结果为:{res}')
        return res
