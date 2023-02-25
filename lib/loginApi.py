from common.rest_client import RestClient
from common.logger import logger


class LoginApi(RestClient):
    def __init__(self, session):
        super().__init__(session)

    def login_user(self, payload):
        res = self.post('/user/login', payload=payload, headers=RestClient.header)
        logger.info(f'用户登录 ==>> 返回结果为:{res.text}')
        return res

