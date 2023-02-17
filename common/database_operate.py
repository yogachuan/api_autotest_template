import pymysql
import os
from common.read_data import ReadFileData
from common.logger import logger

base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = os.path.join(base_path, "config", "setting.yml")
data = ReadFileData.load_yaml(data_file_path)["mysql"]

DB_CONF = {
    "host": data["MYSQL_HOST"],
    "port": int(data["MYSQL_PORT"]),
    "user": data["MYSQL_USER"],
    "password": data["MYSQL_PASSWD"],
    "db": data["MYSQL_DB"]
}


class MysqlDb:

    def __init__(self, db_conf=None):
        # 通过字典拆包传递配置信息，建立数据库连接
        if db_conf is None:
            db_conf = DB_CONF
        self.conn = pymysql.connect(**db_conf, autocommit=True)
        # 通过 cursor() 创建游标对象，并让查询结果以字典格式输出
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):  # 对象资源被释放时触发，在对象即将被删除时的最后操作
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def select_db(self, sql):
        """
        执行查询语句
        :param sql:
        :return:
        """
        # 检查连接是否断开，如果断开就进行重连
        self.conn.ping(reconnect=True)
        # 使用 execute() 执行sql
        self.cur.execute(sql)
        # 使用 fetchall() 获取查询结果
        select_data = self.cur.fetchall()
        return select_data

    def execute_db(self, sql):
        """
        执行更新/新增/删除语句
        :param sql:
        :return:
        """
        try:
            # 检查连接是否断开，如果断开就进行重连
            self.conn.ping(reconnect=True)
            # 使用 execute() 执行sql
            self.cur.execute(sql)
            # 提交事务
            self.conn.commit()
            logger.info(f"操作SQL语句成功[{sql}]")
        except Exception as e:
            logger.info("操作MySQL出现错误，错误原因：{}".format(e))
            # 回滚所有更改
            self.conn.rollback()


db = MysqlDb(DB_CONF)

if __name__ == '__main__':
    insert_user_sql = "INSERT INTO `dangansystem`.`ebz_user`(`USER_UUID`, `USER_CODE`, `USER_NAME`, `SEX`, `SORT`, " \
                      "`CREATE_TIME`) VALUES ('222', 'code2', 'name2', '男', 1, '2022-06-16 15:19:34') "
    db.execute_db(insert_user_sql)
    select_user_sql = "select user_uuid,user_code from ebz_user where user_name='{}'".format("name2")
    result_select = db.select_db(select_user_sql)

    # db.__del__()
    print('--------------{}'.format(result_select))
    print(base_path)
    print('--------end------')
    print('data_file_path:=', data_file_path)
    print('data:=', data)
