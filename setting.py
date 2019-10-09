import os

# 环境路径
PATH = os.path.dirname(os.path.realpath(__file__))

# log等级
log_grade = "error"

# 爬虫设置
spider_name = ""
async_number = 1
function = ""

# rabbitmq
rabbitmq_host = "127.0.0.1"
rabbitmq_user = "fsw"
rabbitmq_pwd = "123456"
# 如果rabbitmq队列里面有数据时是否清除
is_purge = False

# mysql
is_create_sql = False
mysql_host = "127.0.0.1"
mysql_user = "root"
mysql_pwd = "123456"
mysql_port = 3306

# selenium
webdriver_path_win = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

proxies = []