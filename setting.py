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
rabbitmq_pwd = "123456"

# mysql
mysql_host = "127.0.0.1"
mysql_user = "root"
mysql_pwd = "123456"
mysql_port = 3306

# 中间件
MIDDLEWARES = {
    # "wangyiyun_buff": 'tools.middleware.WangYiYunBuff',
    "lagouwang": 'tools.middleware.LaGouWang',
    "bosszhipin": 'tools.middleware.BossZhiPin',
    # 'tools.middleware.DefaultMiddleware': 543,
}

# selenium
webdriver_path_win = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

proxies = [
    # -----------------------------百度云代理
    '106.12.199.35:8089', '106.12.199.151:8089', '106.12.199.161:8089', '106.12.128.78:8089',
    '106.12.31.86:8089', '106.12.83.54:8089', '106.12.133.155:8089', '106.12.128.176:8089', '106.12.89.102:8089',
    '106.12.199.170:8089', '106.12.128.179:8089', '106.12.133.218:8089', '106.12.199.214:8089',
    '106.12.134.175:8089', '106.12.85.211:8089', '106.12.133.224:8089', '106.12.101.33:8089',
    '106.12.210.101:8089', '106.12.202.115:8089', '106.12.101.239:8089', '106.12.89.250:8089', '106.12.90.57:8089',
    '182.61.27.83:8089', '106.12.204.18:8089', '106.12.90.3:8089', '182.61.49.100:8089', '106.12.204.65:8089',
    '106.12.199.181:8089', '106.12.8.69:8089', '106.12.199.193:8089', '106.12.128.100:8089',
    '106.12.128.202:8089'
    # '106.12.134.168:8089','182.61.30.168:8089','106.12.128.102:8089','106.12.133.222:8089',
]