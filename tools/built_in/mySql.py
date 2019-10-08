import pymysql
from DBUtils.PooledDB import PooledDB
import setting
from tools import log
logger = log(__name__)


class MySql:
    def __init__(self, pool):
        self.pool = pool

    @classmethod
    def mysql_pool(cls, dbname=None, mysql_host=None, mysql_port=3306, mysql_user=None, mysql_pwd=None):
        logger.debug("开启mysql连接池！")
        if not mysql_host or not mysql_user or not mysql_pwd:
            host, port, user, password = setting.mysql_host, setting.mysql_port, setting.mysql_user, setting.mysql_pwd
        else:
            host, port, user, password = mysql_host, mysql_port, mysql_user, mysql_pwd
        if not dbname:
            pool = PooledDB(creator=pymysql, maxconnections=5,
                            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                            setsession=[],
                            ping=0,
                            host=host,
                            port=port,
                            user=user,
                            password=password,
                            charset='utf8', )
        else:
            pool = PooledDB(creator=pymysql, maxconnections=5,
                            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                            setsession=[],
                            ping=0,
                            host=host,
                            port=port,
                            user=user,
                            password=password,
                            database=dbname,
                            charset='utf8', )
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

    def select(self, tablename, key=None, value=None, v="*", term=None, one=False):
        conn, cursor = self.open()
        if term:
            sql = 'select {} from {} where {};'.format(v, tablename, term)
        elif key and (value or value == 0):
            sql = 'select {} from {} where {}="{}";'.format(v, tablename, key, value)
        else:
            sql = 'select {} from {};'.format(v, tablename)
        cursor.execute(sql)
        conn.commit()
        if one:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
        self.close(conn, cursor)
        return result

    def delete(self, tablename, key, value):
        conn, cursor = self.open()
        sql = "DELETE FROM {} WHERE {} = '{}';".format(tablename, key, value)
        cursor.execute(sql)
        conn.commit()
        self.close(conn, cursor)

    def update(self):
        pass

    def insql(self, tablename, keys=None, values=None, items=None):
        conn, cursor = self.open()
        if not keys and not items and values:
            count = len(values)
            sql = "INSERT INTO {} VALUES (".format(tablename) + "%s, "*(count-1) + "%s" + ");"
            cursor.execute(sql, values)
            print(values)
            conn.commit()
            self.close(conn, cursor)

        elif not items and keys and values:
            keys = ''.format(str(i) for i in keys)
            count = len(values)
            sql = "INSERT INTO {table_name}({keys}) VALUES (".format(table_name=tablename, keys=keys,)\
                  + "%s, "*(count-1) + "%s" + ");"
            cursor.execute(sql, values)
            print(values)
            conn.commit()
            self.close(conn, cursor)

        elif not keys and not values and items:
            keys = ','.format(str(i) for i in items.keys())
            values = [i for i in items.values()]
            count = len(values)
            sql = "INSERT INTO {table_name}({keys}) VALUES (".format(table_name=tablename, keys=keys,) \
                  + "%s, "*(count-1) + "%s" + ");"
            cursor.execute(sql, values)
            print(values)
            conn.commit()
            self.close(conn, cursor)
        else:
            print("入库失败，字段不符合要求！")

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

    def use_table(self, tablename):
        conn, cursor = self.open()
        sql = "USE %s" % tablename
        cursor.execute(sql)
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
