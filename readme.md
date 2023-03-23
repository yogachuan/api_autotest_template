# python+selenium+unittest+ddt+HTMLTestRunner(以蜗牛进销存登录为例)

*如下代码只是举例，具体以仓库代码为准*

## 一、框架组成

- - common
    公共层放公用的模块
  - config
    配置文件层
  - lib
    接口层
  - case
    测试用例层
  - data
    测试数据层
  - suite
    测试套件层
  - logs
    输出日志
  - report
    输出测试报告

## 二、搭建步骤

### 1、在config层中创建配置文件xml格式

setting.xml

```xml
host:
  api_root_url: "http://43.138.88.28:8080/woniusales"
  api_content_type: "application/x-www-form-urlencoded; charset=UTF-8"

# chrome  or firefox
browserType:
  browser_type: "chrome"

mysql:
  MYSQL_HOST: "43.138.88.28"
  MYSQL_PORT: "12345"
  MYSQL_USER: "root"
  MYSQL_PASSWD: "123456"
  MYSQL_DB: "woniusale"
```

### 2、在common层中写读文件方法

read_data.py

```python
# -*- coding: utf-8 -*-
import yaml
import xlrd
import json
from configparser import ConfigParser
from framework.common.logger import logger


class MyConfigParser(ConfigParser):
    # 重写 configparser 中的 optionxform 函数，解决 .ini 文件中的 键option 自动转为小写的问题
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


class ReadFileData:
    def __init__(self):
        pass

    @staticmethod
    def load_yaml(file_path):
        logger.info("加载 {} 文件......".format(file_path))
        with open(file_path, encoding='gbk') as f:
            data = yaml.safe_load(f)
        logger.info("读到数据 ==>>  {} ".format(data))
        return data

    @staticmethod
    def load_json(file_path):
        logger.info("加载 {} 文件......".format(file_path))
        with open(file_path, encoding='gbk') as f:
            data = json.load(f)
        logger.info("读到数据 ==>>  {} ".format(data))
        return data

    @staticmethod
    def load_ini(file_path):
        logger.info("加载 {} 文件......".format(file_path))
        config_parser = MyConfigParser()
        config_parser.read(file_path, encoding="UTF-8")
        data = dict(config_parser._sections)
        print("读到数据 ==>>  {} ".format(data))
        return data
      
    @staticmethod
    def load_excel(file_path):
        file = xlrd.open_workbook(file_path)
        sheet = file.sheet_by_index(0)
        data = []
        for row in range(1, sheet.nrows):
            lines = []
            for col in range(1, sheet.ncols):
                value = sheet.cell(row, col).value
                if not isinstance(value, str):
                    # 单元格内容不是字符串类型
                    value = str(int(value))
                lines.append(value)
            data.append(lines)
        return data

read_data = ReadFileData()

if __name__ == '__main__':
    import os

    base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    userdata = ReadFileData.load_yaml(os.path.join(base_path, "data", "login_data.yml"))

```

### 3、在common层中写入getSession方法

单例模式，并创建login的类方法，在浏览器打开后直接登录（根据用例判定，如果是登录测试用例，则不执行login方法）

getSession.py

```python
# 创建持久会话
import requests
from common.logger import logger
import os
from common.rest_client import RestClient


class GetSessionID:
    # 创建一个静态属性
    ses = None
    base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    api_root_url = RestClient.api_root_url
    api_content_type = RestClient.api_content_type

    @classmethod
    def sessionMethod(cls, case='notLogin'):
        if cls.ses is None:
            cls.ses = requests.Session()
            # 生成会话之后调用登录方法
            if case == 'notLogin':
                # 非登录类用例需先执行登录操作
                GetSessionID.login()
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
```

### 4、在common层中创建写日志方法

logger.py（细读）

```python
# -*- coding: utf-8 -*-

import logging
import os
import time


class Logger(object):

    def __init__(self, logger_name=None):
        """
        指定保存日志的文件路径，日志级别，以及调用文件
        将日志存入到指定的文件中
        """
        # 日志文件夹，如果不存在则自动创建
        cur_path = os.path.dirname(os.path.realpath(__file__))
        log_path = os.path.join(os.path.dirname(cur_path), f'logs')
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        # log 日期文件夹
        now_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        phone_log_path = os.path.join(os.path.dirname(cur_path), f'logs\\{now_date}')
        if not os.path.exists(phone_log_path):
            os.mkdir(phone_log_path)
        # 创建一个logger
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        # 创建一个handler，用于写入日志文件
        now_time = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
        log_name = os.path.join(phone_log_path, f'{now_time}.log')
        fh = logging.FileHandler(log_name)
        fh.setLevel(logging.INFO)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s %(filename)s [line:%(lineno)d]: %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getLog(self):
        return self.logger
logger = Logger().logger
```

### 5、在common层中封装restclient基类

rest_client.py（封装请求，post、get、put等等）

​	*类初始化时需传入session*

```python
import json
import json as cjson
from common.logger import logger
from common.read_data import read_data
import os


class RestClient:
    basepath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    print(basepath)
    file_data = read_data.load_yaml(os.path.join(basepath, 'config', 'setting.yml'))['host']
    api_root_url = file_data["api_root_url"]
    api_content_type = file_data["api_content_type"]

    def __init__(self, session):
        self.ses = session

    def request(self, url, method, payload=None, **kwargs):
        url = self.api_root_url + url
        headers = dict(**kwargs).get('headers')
        params = dict(**kwargs).get('params')
        files = dict(**kwargs).get('files')
        self.request_log(url, method, headers, payload, params, files)
        if method.upper() == 'POST':
            if self.api_content_type is None:
                return self.ses.post(url, data=json.dumps(payload), **kwargs)
            if self.api_content_type.__contains__("application/x-www-form-urlencoded"):
                return self.ses.post(url, data=payload, **kwargs)
            if self.api_content_type.__contains__("application/json"):
                return self.ses.post(url, json=payload, **kwargs)
        if method.upper() == 'GET':
            return self.ses.get(url, **kwargs)
        if method.upper() == 'PUT':
            data = ''
            if json:
                # PUT 和 PATCH 中没有提供直接使用json参数的方法，因此需要用data来传入
                data = cjson.dumps(json)
            return self.ses.put(url, data, **kwargs)

        if method.upper() == 'DELETE':
            return self.ses.delete(url, **kwargs)
        if method.upper() == 'PATCH':
            data = ''
            if json:
                data = cjson.dumps(json)
            return self.ses.patch(url, data, **kwargs)

    def request_log(self, url, method, headers=None, data=None, params=None, files=None, **kwargs):
        """记录请求日志"""
        # Python3中，json在做dumps操作时，会将中文转换成unicode编码，因此设置 ensure_ascii=False
        logger.info(f'接口请求地址 ==>> {url}')
        logger.info(f'接口请求方式 ==>> {method}')
        logger.info(f'接口请求头 ==>> {cjson.dumps(headers, indent=4, ensure_ascii=False)}')
        logger.info(f'接口请求 params 参数 ==>> {cjson.dumps(params, indent=4, ensure_ascii=False)}')
        logger.info(f'接口上传附件 files 参数 ==>> {files}')
        logger.info(f'接口请求体 data 参数 ==>> {cjson.dumps(data, indent=4, ensure_ascii=False)}')

    def get(self, url, **kwargs):
        return self.request(url, 'get', **kwargs)

    def post(self, url, payload=None, **kwargs):
        return self.request(url, 'post', payload, **kwargs)

    def put(self, url, payload=None, **kwargs):
        return self.request(url, 'put', payload, **kwargs)

    def patch(self, url, payload=None, **kwargs):
        return self.request(url, 'patch', payload, **kwargs)

    def delete(self, url, **kwargs):
        return self.request(url, 'delete', **kwargs)

```

### 6、在lib层中创建接口对象

loginApi.py（继承自RestClient），所以在实例化该类时需传入session。

获取结果文本用于校验，将结果文本作为方法的返回（代码最后）*

```python
from common.rest_client import RestClient
from common.logger import logger


class LoginApi(RestClient):
    def __init__(self, session):
        super().__init__(session)
        self.header = {
            'Content-Type': self.api_content_type
        }
		# 这种方式适合接口参数较少时使用，但是一旦某个接口的参数需要10几个点的时候，用这种形参就会非常麻烦，而且一旦接口参数被修改，相应的以下测试方法也要修改
    # def login_user(self, usr, pwd, code):
    #     payload = {
    #         'username': usr,
    #         'password': pwd,
    #         'verifycode': code
    #     }
    #     res = self.post('/user/login', payload=payload, headers=self.header)
    #     logger.info(f'用户登录 ==>> 返回结果为:{res.text}')
    #     return res
    
    # 这种方法适用于接口参数较多时使用，直接将接口参数打包成payload，减少了测试方法的传参数量，而且以后一旦接口参数被修改，测试方法的形参也不用修改，只需要对测试用例中的参数进行修改即可
    def login_user(self, payload):
        res = self.post('/user/login', payload=payload, headers=self.header)
        logger.info(f'用户登录 ==>> 返回结果为:{res.text}')
        return res



```

### 7、在case层中创建测试用例

在用例中创建浏览器并实例化lib层中的接口对象，实例化时需传入session

test_login.py（继承自unittest.TestCase）

​	1.*setUpClass、tearDownClass、setUp、tearDown细读*

​	2.*在setUp中调用session（调用时需判断用例是不是登录测试用例），并实例化页面对象，实例化时传入该浏览器*

​			登录用例：

​				*GetSessionID.sessionMethod(case='login')*

​			非登录用例：

​				*GetSessionID.sessionMethod()*

​	3.在tearDown中做一些清除操作，可以在teardown中执行一些sql

<!--在setupClass还是setUp中初始化浏览器均可，根据业务流程进行选择，最好是setUp中初始化浏览器-->

​	4.*test_login，真正执行用例的地方，必须以“test_”开头*

​	5.*使用ddt将输入参数传入*

```python
from ddt import ddt, data, unpack
@ddt
class AAA:
  info = []
  //info为数据列表，data方法可将info列表打散并传入test_aaa方法所需参数中
  @data(*info)
  @unpack()
  def test_aaa(self,a,b,c):
    
```

```python
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
    case_data = read_data.load_yaml(os.path.join(base_path, 'data', 'login.yml'))
    logger.info(f'登录类测试用例数据为{case_data["login_nor_data"]}')

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

    @data(*case_data["login_nor_data"])
    @unpack
    # case_data["login_nor_data"]解包后的键名要和以下测试方法中的形参名一致，否则报错
    def test_login_success(self, case_name, case_desc, payload, expect_msg):
        logger.info(f'用例名{case_name},用例描述{case_desc}')
        res = self.login_api.login_user(payload)
        # res_json = res.json()
        print(f"res:{res.text}")
        self.assertIn(expect_msg, res.text)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(LoginTest())
    runner = unittest.TextTestRunner()
    test_result = runner.run(suite)

```

## 8、data层创建yml格式的用例

Login.yml

```yaml
login_nor_data:
  - case_name: "login_nor001"
    case_desc: "用户admin登录成功"
    payload: {
      username: "admin",
      password: "123456",
      verifycode: '0000'
    }
    expect_msg: "pass"

  - case_name: "login_nor002"
    case_desc: "用户lm登录成功"
    payload: {
      username: "lm",
      password: "lmlm123",
      verifycode: '0000'
    }
    expect_msg: "pass"

login_abn_data:
  - case_name: "login_abn001"
    case_desc: "用户admin登录失败"
    payload: {
      username: "admin",
      password: "lmlm123",
      verifycode: '0000'
    }
    expect_msg: "fail"
```

customer_add.yml

```yml
customer_add_nor_data:
  - case_name: "customer_add_nor001"
    case_desc: "添加用户yujia1成功"
    payload: {
      customername: 'yujia1',
      customerphone: '13292679673',
      childsex: '男',
      childdate: '1993-10-20',
      creditkids: '0',
      creditcloth: '0'
    }
    expect_msg: "success"

  - case_name: "customer_add_nor002"
    case_desc: "添加用户yujia1成功"
    payload: {
      customername: 'yujia2',
      customerphone: '13292679674',
      childsex: '男',
      childdate: '1993-10-20',
      creditkids: '0',
      creditcloth: '0'
    }
    expect_msg: "success"

customer_add_abn_data:
```

