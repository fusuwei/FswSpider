from tools.built_in.mySql import MySql
import setting
proxy = setting.proxies


def get_ip(mysql=None, ):
    if not mysql:
        mysql = MySql.mysql_pool(dbname="proxypool", mysql_host="127.0.0.1", mysql_user="root", mysql_pwd="123456")
    conn, cursor = mysql.open()
    sql = "show tables"
    cursor.execute(sql)
    result = [i["Tables_in_proxypool"] for i in cursor.fetchall()]
    if "Proxies" in result or "proxies" in result:
        proxies = mysql.select("Proxies")
        proxies = ["https://%s:%s" % (ip["addr"], ip["port"]) if ip["ip_type"] and ("https" in ip["ip_type"] or "HTTPS"
                                                                                    in ip["ip_type"])
                   else"http://%s:%s" % (ip["addr"], ip["port"]) for ip in proxies]
        setting.proxies.extend(proxies)


if __name__ == '__main__':
    get_ip()