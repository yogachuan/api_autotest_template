# 创建持久会话
import requests
from common.logger import logger
import os
from common.read_data import read_data


class GetSessionID:
    # 创建一个静态属性
    ses = None
    base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    print(base_path)
    file_data = read_data.load_yaml(os.path.join(base_path, 'config', 'setting.yml'))['host']
    api_root_url = file_data["api_root_url"]
    api_content_type = file_data["api_content_type"]

    @classmethod
    def sessionMethod(cls, case='notLogin'):
        if cls.ses is None:
            cls.ses = requests.Session()
            # 生成会话之后调用登录方法
            if case == 'notLogin':
                # 非登录类用例需先执行登录操作
                GetSessionID.login()
            else:
                # 登录类用例
                pass

        return cls.ses

    @classmethod
    def login(cls):
        logger.info(f'非登录类测试用例需先进行登录操作')
        url = cls.api_root_url + '/user/login'
        head = {
            'Content-Type': cls.api_content_type
        }
        payload = {
            'username': 'admin',
            'password': '123456',
            'verifycode': '0000'
        }
        res = cls.ses.post(url=url, headers=head, data=payload)
        # print(f'res:{res.text}')
        logger.info('登录用户为[admin]')


