import pymysql
from DBUtils.PooledDB import PooledDB
import setting
from tools import log
logger = log(__name__)


class MySql:
    def __init__(self, pool):
        self.pool = pool
        self.sql = Sql()

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

    def select(self, tablename, keys, conditions, isdistinct=0, limit=None, order_by=None, one=False):
        sql = self.sql.get_s_sql(tablename, keys, conditions, isdistinct, limit, order_by,)
        conn, cursor = self.open()
        cursor.execute(sql)
        conn.commit()
        if one:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
        self.close(conn, cursor)
        return result

    def delete(self, tablename, conditions):
        sql = self.sql.get_d_sql(tablename, conditions)
        conn, cursor = self.open()
        cursor.execute(sql)
        conn.commit()
        self.close(conn, cursor)

    def update(self, tablename, value, conditions):
        sql = self.sql.get_u_sql( tablename, value, conditions)
        conn, cursor = self.open()
        cursor.execute(sql)
        conn.commit()
        self.close(conn, cursor)

    def insql(self, tablename, conditions):
        sql = self.sql.get_i_sql(tablename, conditions)
        conn, cursor = self.open()
        cursor.execute(sql)
        conn.commit()
        print("入库信息：", conditions)
        self.close(conn, cursor)

    def diy_sql(self, sql):
        conn, cursor = self.open()
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
        self.close(conn, cursor)
        return result

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


class Sql:
    def __init__(self):
        pass

    def get_i_sql(self, table, dict):
        '''
        生成insert的sql语句
        @table，插入记录的表名
        @dict,插入的数据，字典
        '''
        sql = 'insert into %s set ' % table
        sql += self.dict_2_str(dict)
        return sql

    def get_s_sql(self, table, keys, conditions, isdistinct=0, limit=None, order_by=None):
        '''
            生成select的sql语句
        @table，查询记录的表名
        @key，需要查询的字段
        @conditions,插入的数据，字典
        @isdistinct,查询的数据是否不重复
        '''
        if isdistinct:
            sql = 'select distinct %s ' % ",".join(keys)
        else:
            sql = 'select  %s ' % ",".join(keys)
        sql += ' from %s ' % table
        if conditions:
            sql += ' where %s ' % self.dict_2_str_and(conditions)
        if limit:
            if isinstance(limit, int):
                sql += ' limit %s ' % limit
            elif isinstance(limit, list) or isinstance(limit, tuple):
                sql += ' limit %s,%s ' % limit
        if order_by:
            order_by = pymysql.escape_dict(order_by, 'utf8')
            tmp = ''
            for k, v in order_by.items():
                tmp += "%s,%s " % (str(k), str(v))
            sql += ' order by %s' % tmp
        return sql

    def get_u_sql(self, table, value, conditions):
        '''
            生成update的sql语句
        @table，查询记录的表名
        @value，dict,需要更新的字段
        @conditions,插入的数据，字典
        '''
        sql = 'update %s set ' % table
        sql += self.dict_2_str(value)
        if conditions:
            sql += ' where %s ' % self.dict_2_str_and(conditions)
        return sql

    def get_d_sql(self, table, conditions):
        '''
            生成detele的sql语句
        @table，查询记录的表名

        @conditions,插入的数据，字典
        '''
        sql = 'delete from  %s  ' % table
        if conditions:
            sql += ' where %s ' % self.dict_2_str_and(conditions)
        return sql

    def dict_2_str(self, dictin):

        '''
        将字典变成，key='value',key='value' 的形式
        '''
        tmplist = []
        for k, v in dictin.items():
            tmp = "%s='%s'" % (str(pymysql.escape_string(k)), str(pymysql.escape_string(v)))
            tmplist.append(' ' + tmp + ' ')
        return ','.join(tmplist)

    def dict_2_str_and(self, dictin):
        dictin = pymysql.escape_dict(dictin, "utf8")
        '''
        将字典变成，key='value' and key='value'的形式
        '''
        tmplist = []
        for k, v in dictin.items():
            tmp = "%s='%s'" % (str(pymysql.escape_string(k)), str(pymysql.escape_string(v)))
            tmplist.append(' ' + tmp + ' ')
        return ' and '.join(tmplist)