import json
import json as cjson
from common.logger import logger
from common.read_data import read_data
import os


class RestClient:
    base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    # print(basepath)
    file_data = read_data.load_yaml(os.path.join(base_path, 'config', 'setting.yml'))['host']
    api_root_url = file_data["api_root_url"]
    api_content_type = file_data["api_content_type"]
    header = {
        'Content-Type': api_content_type
    }

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

