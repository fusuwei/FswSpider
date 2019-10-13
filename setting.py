import os

# 环境路径
PATH = os.path.dirname(os.path.realpath(__file__))

# log等级
log_grade = "warning"

# 爬虫设置
spider_name = ""
async_number = 1
function = ""

# rabbitmq
rabbitmq_host = "127.0.0.1"
rabbitmq_user = "fsw"
rabbitmq_pwd = "fsw.1996"

# mysql
mysql_host = "127.0.0.1"
mysql_user = "root"
mysql_pwd = "fsw.1996"
mysql_port = 3306

# selenium
webdriver_path_win = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

proxies = []