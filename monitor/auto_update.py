from tools import mysqlconnecting
import multiprocessing
from manager.runner import run
import requests
import time
import setting


def get_update_program(auto_mysql,
                       rabbitmq_host, rabbitmq_user, rabbitmq_pwd
                       ):
    programs = []
    items = auto_mysql.select('auto_update', '*', {"success": 1, "auto_update": 1})
    for item in items:
        update_freq = item["update_freq"]
        if not update_freq:
            continue
        else:
            updated = int(time.mktime(time.strptime(str(item["updated"]), "%Y-%m-%d %H:%M:%S")))
            if time.time()-updated < float(update_freq)*3600:
                continue
            name = item['name']
            try:
                res = requests.get(
                    url='http://{}:{}/api/queues/{}/{}'.format(rabbitmq_host, "15672", "%2F", name),
                    auth=(rabbitmq_user, rabbitmq_pwd)
                )
            except Exception as e:
                continue
            else:
                if res.status_code == 404:
                    programs.append(item)
    return programs


if __name__ == '__main__':
    db = "spider_auto_update"
    mysql_host = setting.mysql_host
    mysql_user = setting.mysql_user
    mysql_pwd = setting.mysql_pwd
    mysql_port = setting.mysql_port
    rabbitmq_host = setting.rabbitmq_host
    rabbitmq_user = setting.rabbitmq_user
    rabbitmq_pwd = setting.rabbitmq_pwd
    auto_mysql = mysqlconnecting(db, mysql_host, mysql_user, mysql_pwd,
                                 mysql_port=mysql_port, maxconnections=1)[0]
    while True:

        programs = get_update_program(auto_mysql, rabbitmq_host, rabbitmq_user, rabbitmq_pwd)

        if programs:
            if len(programs) < 10:
                pool = multiprocessing.Pool(len(programs))
            else:
                pool = multiprocessing.Pool(10)
            for program in programs:
                pool.apply_async(run, args=(program["path_name"], True, ))
            pool.close()
            pool.join()
        time.sleep(8)
        print("等待8s..")