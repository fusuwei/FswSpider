import os


PATH = os.path.dirname(os.path.realpath(__file__))


spider_name = ""
async_number = 1
function = "m"

# rabbitmq
rabbitmq_host = "127.0.0.1"
rabbitmq_user = "fsw"
rabbitmq_pwd = "123456"

EXCHANGE = 'spider'
ROUTING_KEY = 'spider.message'
EXCHANGE_TYPE = 'topic'
PUBLISH_INTERVAL = 1



# mysql
mysql_host = "127.0.0.1"
mysql_pwd = "123456"
