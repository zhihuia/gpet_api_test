import psycopg2
import configparser
from common import dir_config


class DoPgsql:

    def __init__(self, configfilePath):
        # 读取配置文件
        cf = configparser.ConfigParser()
        cf.read(configfilePath)
        host = cf.get("pgsql_info", "host")
        port = cf.getint("pgsql_info", "port")
        db = cf.get("pgsql_info", "db")
        username = cf.get("pgsql_info", "username")
        passwd = cf.get("pgsql_info", "passwd")
        self.conn = psycopg2.connect(host=host, port=port, database=db, user=username, password=passwd)
        self.cursor = self.conn.cursor()
        print("连接数据库成功！")

    # 查询数据,返回查询结果列表
    def select_data(self, select_sql, params=None):
        print("查询数据的sql语句：")
        print(select_sql)
        self.cursor.execute(select_sql, params)
        select_result = self.cursor.fetchall()
        return select_result[0][0]

    # 关闭数据库连接
    def close_conn(self):
        print("关闭数据库连接。")
        self.cursor.close()
        self.conn.close()
        print("关闭数据库成功！")


temp = DoPgsql(dir_config.dbconfig_dir)
id = temp.select_data("select id from robot where wechat_no = 'yrtLdPpuTwLo';")
print(id)
temp.close_conn()