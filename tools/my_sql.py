import pymysql
from DBUtils.PooledDB import PooledDB
import setting
from tools import log
logger = log(__name__)


class MySql:
    def __init__(self, pool):
        self.pool = pool

    @classmethod
    def mysql_pool(cls):
        logger.debug("开启mysql连接池！")
        pool = PooledDB(creator=pymysql, maxconnections=5,
                        blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                        setsession=[],
                        ping=0,
                        host=setting.mysql_host,
                        port=setting.mysql_port,
                        user=setting.mysql_user,
                        password=setting.mysql_pwd,
                        charset='utf8',)
        return cls(pool)

    def open(self):
        logger.debug("启动mysql连接！")
        conn = self.pool.connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        return conn, cursor

    def close(self, conn, cursor):
        """关闭连接"""
        logger.debug("关闭连接！")
        cursor.close()
        conn.close()

    def select(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def insql(self):
        pass

    def create_db(self):
        if hasattr(setting, "db_dict"):
            db_dict = getattr(setting, "db_dict")
            db_name = db_dict["db"]
            logger.debug("建立数据库%s " % db_name)
            character = db_dict["character"]
            if character in ["utf8", "UTF8", "utf-8", "UTF-8"]:
                character = "utf8mb4"
            sql = r"create database if not exists {} character set {};".format(db_name, character)
            conn, cursor = self.open()
            cursor.execute(sql,)
            sql = self.create_table(db_name, cursor)
            cursor.execute(sql, )
            conn.commit()
            self.close(conn, cursor)

    def create_table(self, db_name, cursor):
        if hasattr(setting, "tb_dict"):
            use_sql = "use {}".format(db_name)
            cursor.execute(use_sql)
            tb_dict = getattr(setting, "tb_dict")
            table_name = tb_dict["table_name"]
            charset = tb_dict["charset"]
            if charset in ["utf8", "UTF8", "utf-8", "UTF-8"]:
                charset = "utf8mb4"
            comment = tb_dict["comment"]
            engine = tb_dict["engine"]
            primary_key = tb_dict["primary_key"]
            index = tb_dict.get("index", "")
            tb_dict.pop("table_name")
            tb_dict.pop("charset")
            tb_dict.pop("comment")
            tb_dict.pop("engine")
            tb_dict.pop("primary_key")
            tb_dict.pop("index")
            sql1 = "create table if not exists {}".format(table_name)
            sql2 = "{},".format(primary_key)
            sqls = []
            sql3 = ''
            if tb_dict:
                for key, evl in tb_dict.items():
                    sqls.append("{} {},".format(key, evl))
                if index:
                    sql3 = 'index info({})'.format(index)
            sql4 = "engine = {} default charset = {} comment = '{}';".format(engine, charset, comment)
            sql = sql1 + "(" + sql2 + "".join(sqls) + sql3 + ")" + sql4
            logger.debug("建立表%s " % table_name)
            return sql
