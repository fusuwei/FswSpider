from tools import mysqlconnecting
import pymysql
import setting


class Init:
    def __init__(self, mysql_host, mysql_user, mysql_pwd, mysql_port):
        self.mysql_host = mysql_host
        self.mysql_user = mysql_user
        self.mysql_pwd = mysql_pwd
        self.mysql_port = mysql_port

    def conn(self):
        self.mysql = mysqlconnecting("spider_auto_update", self.mysql_host, self.mysql_user, self.mysql_pwd,
                                     mysql_port=self.mysql_port, maxconnections=1)[0]
        self.mysql.open()