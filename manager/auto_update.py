from tools import mysqlconnecting
import multiprocessing
from manager.runner import run
import requests
import time


def auto_update(item, pool):
    if not item:
        return
    else:
        pass


def get_update_program(db,  mysql_host, mysql_user, mysql_pwd, mysql_port,
                       rabbitmq_host, rabbitmq_user, rabbitmq_pwd
                       ):
    programs = []
    auto_mysql = mysqlconnecting(db, mysql_host, mysql_user, mysql_pwd,
                                 mysql_port=mysql_port, maxconnections=1)[0]
    items = auto_mysql.select('update', '*', )
    for item in items:
        name =item['name']
        try:
            res = requests.get(
                url='http://{}:{}/api/queues/{}/{}'.format(rabbitmq_host, "15672", "%2F", name),
                auth=(rabbitmq_user, rabbitmq_pwd)
            )
        except Exception as e:
            continue
        else:
            if res.status_code == 200:
                programs.append(item)
    return programs


if __name__ == '__main__':
    while True:
        db = ""
        mysql_host = ""
        mysql_user = ""
        mysql_pwd = ""
        mysql_port = ""
        rabbitmq_host = ""
        rabbitmq_user = ""
        rabbitmq_pwd = ""
        programs = get_update_program(db,  mysql_host, mysql_user, mysql_pwd, mysql_port,
                                      rabbitmq_host, rabbitmq_user, rabbitmq_pwd)

        if programs:
            if len(programs)<10:
                pool = multiprocessing.Pool(len(programs))
            else:
                pool = multiprocessing.Pool(10)
            for program in programs:
                pool.apply_async(run, args=(program["path_name"]))
            pool.close()
            pool.join()
        time.sleep(8)