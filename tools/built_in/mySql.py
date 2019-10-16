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
        sql = self.sql.get_u_sql(tablename, value, conditions)
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

    def use_table(self, tablename):
        conn, cursor = self.open()
        sql = "USE %s" % tablename
        cursor.execute(sql)
        conn.commit()
        self.close(conn, cursor)

    def create_table(self, table_name, conditions):
        sql1 = """CREATE TABLE %s ( 
                        id int primary key AUTO_INCREMENT, 
                        """ % table_name
        tmp = ""
        for k, v in conditions.items():
            if isinstance(v, int):
                tmp += " %s int ," % k
            elif isinstance(v, str) and len(v) < 200:
                tmp += " %s varchar(%s) ," % (k, len(v)+50)
            elif isinstance(v, str) and len(v) > 200:
                tmp += " %s text ," % k
        tmp = tmp.replace(",", ")")
        sql2 = "ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4"
        sql = sql1 + tmp + sql2
        conn, cursor = self.open()
        cursor.execute(sql)
        conn.commit()
        self.close(conn, cursor)


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
            tmp = "%s='%s'" % (pymysql.escape_string(str(k)), pymysql.escape_string(str(v)))
            tmplist.append(' ' + tmp + ' ')
        return ','.join(tmplist)

    def dict_2_str_and(self, dictin):
        dictin = pymysql.escape_dict(dictin, "utf8")
        '''
        将字典变成，key='value' and key='value'的形式
        '''
        tmplist = []
        for k, v in dictin.items():
            tmp = "%s='%s'" % (pymysql.escape_string(str(k)), pymysql.escape_string(str(v)))
            tmplist.append(' ' + tmp + ' ')
        return ' and '.join(tmplist)

async def save(mysql, mes, method, table_name, loop):
    """
    存储函数，负责吧爬下的数据存到mysql数据库中
    :return:
    """
    if method == "insql":
        await loop.run_in_executor(None, mysql.insql, table_name, mes)
    if method == "update":
        values = mes["values"]
        conditions = mes["conditions"]
        await loop.run_in_executor(None, mysql.update, table_name, values, conditions)
    if method == "delete":
        await loop.run_in_executor(None, mysql.delete, table_name, mes)
    if method == "select":
        pass