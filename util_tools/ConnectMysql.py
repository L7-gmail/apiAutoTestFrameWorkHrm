import pymysql

from config.setting import FILE_PATH
from util_tools.ConfigParser import ConfigParser
from util_tools.log_util.RecordLog import logs

conf = ConfigParser(FILE_PATH.get("config_ini"))


class ConnectMysql:
    connect = None
    conf = None

    def __init__(self):
        self.conf = {
            'host': conf.get_section_mysql('host'),
            'port': int(conf.get_section_mysql('port')),
            'user': conf.get_section_mysql('user'),
            'password': conf.get_section_mysql('password'),
            'database': conf.get_section_mysql('database'),
            'charset': conf.get_section_mysql('charset')
        }

    def get_connect(self):
        if self.connect is None:
            try:
                self.connect = pymysql.connect(**self.conf)
                return self.connect
            except Exception as e:
                logs.error(f"连接数据库异常：{str(e)}")
        return self.connect

    def close_connect(self):
        if self.connect is not None:
            self.connect.close()

    def query(self, sql, fellAll=True, close_connect=True):
        """
        数据库查询
        :param sql: sql
        :param fellAll: 如果是False查询一条语句，如果是True查询全部语句
        :param close_connect: 是否执行完这条sql后就关闭数据库连接
        :return: 返回查询结果
        """
        connect = None
        cursor = None
        result = None
        try:
            connect = self.get_connect()
            cursor = connect.cursor()
            cursor.execute(sql)
            if fellAll:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone()
            logs.info(f"查询数据成功：{result},sql：{sql}")
            cursor.close()
            return result
        except Exception as e:
            logs.error(f"查询数据库异常：{str(e)}")
        finally:
            if close_connect:
                self.close_connect()

    def upd_del_add(self, sql, close_connect=True):
        """
        数据库增删改操作
        :param sql: sql语句
        :param close_connect: 是否执行完这条sql后就关闭数据库连接
        """
        connect = None
        cursor = None
        try:
            connect = self.get_connect()
            cursor = connect.cursor()
            cursor.execute(sql)
            connect.commit()
            logs.info(f"增删改数据成功,sql: {sql}")
            cursor.close()
        except Exception as e:
            logs.error(f"操作数据库增删改异常：{str(e)}")
        finally:
            if close_connect:
                self.close_connect()


if __name__ == '__main__':
    connect_mysql = ConnectMysql()
    # result = connect_mysql.query('select * from ecs_users',fellAll=True)
    # print(result)
    connect_mysql.upd_del_add("delete from ecs_users where email = '1231@qq.com' and user_name = 'test' ")
