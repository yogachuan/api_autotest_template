# -*- coding: utf-8 -*-
import yaml
import json
from configparser import ConfigParser
from common.logger import logger
import xlrd


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
        with open(file_path, encoding='UTF-8') as f:
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
            for col in range(sheet.ncols):
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
