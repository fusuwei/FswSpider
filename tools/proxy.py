from tools.built_in.mySql import MySql
import setting
import random
proxy = setting.proxies


def get_ip(mysql=None):
    if mysql:
        # mysql = MySql.mysql_pool(dbname="proxypool", mysql_host="127.0.0.1", mysql_user="root", mysql_pwd="123456")
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
    if setting.proxies:
        if len(setting.proxies) == 1:
            return setting.proxies[0]
        return random.choice(setting.proxies)


def ip_process(proxies=None, is_async=True):
    if proxies:
        if is_async:
            if proxies and isinstance(proxies, str):
                proxies = "http://" + proxies.replace("http://", '').replace("https://", '')
                return proxies
            else:
                raise ValueError("代理格式不对！")
        else:
            if proxies and isinstance(proxies, str):
                if "https" in proxies:
                    proxies = {"https": proxies}
                elif "http" in proxies:
                    proxies = {"http": proxies}
                else:
                    proxies = {"http": "http://" + proxies}
            else:
                raise ValueError("代理格式不对！")
            return proxies
