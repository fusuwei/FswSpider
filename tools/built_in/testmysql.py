from sqlalchemy import MetaData, create_engine, Table
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import setting
import pymysql


class MySql:

    def __init__(self, engine, is_create_sql):
        self.engine = engine
        self.is_create_sql = is_create_sql

    @classmethod
    def connect(cls, dbname, tablename, is_create_sql=False):
        conn = pymysql.connect(host=setting.mysql_host, user=setting.mysql_user, password=setting.mysql_pwd,
                               charset="utf8")
        cursor = conn.cursor()
        sql = r"create database if not exists {} character set {};".format(dbname, "utf8mb4")
        cursor.execute(sql, )
        conn.commit()
        cursor.close()
        conn.close()
        url = "mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}".format(username=setting.mysql_user,
                                                                                    password=setting.mysql_pwd,
                                                                                    host=setting.mysql_host,
                                                                                    port=3306,
                                                                                    dbname=dbname
                                                                                    )
        engine = create_engine(url, echo=False)
        return cls(engine, is_create_sql)

