import tools
from tools.built_in.middleware import middleware
from queue import Queue
from threading import Thread
import time
import abc
import asyncio
import setting
import json
import traceback
import os
logger = tools.log(__name__)
PATH = setting.PATH


class Spider:
    def __init__(self):
        # 爬虫脚本配置
        self.auto_proxy = False
        self.auto_cookies = False
        self.auto_headers = True
        self.allow_code = []
        self._url_md5 = set()
        self.is_async = True
        self.cookies = None
        self.session = None

        # 数据库配置
        self.mysql_host = "127.0.0.1"
        self.mysql_user = "root"
        self.mysql_pwd = ""
        self.mysql_port = 3306
        self.dbname = "FswSpider"
        self.table_name = ""

        # RabbitMq配置
        self.rabbitmq_host = "127.0.0.1"
        self.rabbitmq_user = "root"
        self.rabbitmq_pwd = ""
        self.is_purge = False

        self._pre_domain_name = None

        self._result_queue = Queue()

    def init(self):
        """
        初始化函数， mysql, RabbitMq 连接, 其他配置
        :return:
        """
        # 爬虫配置初始化
        self.spider_name = setting.spider_name
        if not self.spider_name:
            pass
        self.function = setting.function
        if not self.function:
            self.function = "w"

        self.async_number = setting.async_number
        if not self.async_number:
            self.async_number = 1

        # mysql连接
        if not self.table_name:
            self.table_name = self.spider_name
        if self.dbname:
            if not self.mysql_host:
                self.mysql_host = setting.mysql_host
            if not self.mysql_user:
                self.mysql_user = setting.mysql_user
            if not self.mysql_pwd:
                self.mysql_pwd = setting.mysql_pwd
                if not self.mysql_pwd:
                    logger.error("没有mysql密码！")
                    os._exit(-1)
            if not self.mysql_port:
                self.mysql_port = setting.mysql_port
            self.Mysql = tools.MySql.mysql_pool(dbname=self.dbname, mysql_host=self.mysql_host, mysql_port=self.mysql_port,
                                          mysql_user=self.mysql_user, mysql_pwd=self.mysql_pwd
                                          )
            self.insql = self.Mysql.insql
            self.delete = self.Mysql.delete
            self.select = self.Mysql.select
            self.update = self.Mysql.update

            show_table_sql = "show tables"
            result = self.Mysql.diy_sql(show_table_sql)
            self.tables = [i["Tables_in_%s" % self.dbname] for i in result]

        else:
            logger.error("请配置数据库苦命")
            os._exit(-1)
        # rabbitmq连接
        if self.spider_name:
            if not self.rabbitmq_host:
                self.rabbitmq_host = setting.rabbitmq_host
            if not self.rabbitmq_user:
                self.rabbitmq_user = setting.rabbitmq_user
            if not self.rabbitmq_pwd:
                self.rabbitmq_pwd = setting.rabbitmq_pwd
                if not self.rabbitmq_pwd:
                    logger.error("RabbitMq密码！")
                    os._exit(-1)
            self.Rabbit = tools.RabbitMq.connect(self.spider_name)

        # 其他参数
        self._produce_count = 1
        self.selector = tools.selector
        self.new_loop = asyncio.new_event_loop()
        self.save_loop = asyncio.new_event_loop()

    def produce(self, message=None):
        """
        生产函数，把爬虫数据存到RabbitMq中
        :param message: list 爬虫数据
        :return:
        """
        logger.debug("开始生产！")
        if self.function == "m":
            if hasattr(self, "start_produce"):
                start_produce = getattr(self, "start_produce")
                if self.Rabbit.queue.method.message_count and self.is_purge:
                    self.Rabbit.purge(self.spider_name)
                for i, message in enumerate(start_produce()):
                    md5 = tools.get_md5([message.get("url", ""), message.get("data", '')])
                    if md5 not in self._url_md5:
                        print("[%d]生产：" % (i+1), message)
                        message = json.dumps(message)
                        self.Rabbit.pulish(message)
                        self._url_md5.add(md5)

        elif self.function == "w":
            md5 = tools.get_md5([message.get("url", ""), message.get("data", '')])
            if md5 not in self._url_md5:
                print("[%d]生产：" % (self._produce_count + 1), message)
                message = json.dumps(message)
                self.Rabbit.pulish(message)

    def consume(self):
        """
        消费函数
        :return:
        """
        # heartbeat = Heartbeat(self.rabbit.connection)  # 实例化一个心跳类
        # heartbeat.start()  # 开启一个心跳线程，不传target的值默认运行run函数
        # heartbeat.startheartbeat()  # 开启心跳保护
        self.Rabbit.consume(callback=self.callback, limit=self.async_number)
        self.Rabbit.del_queue(self.spider_name)
        tools.close_session(self.session, is_async=self.is_async)
        self._result_queue.join()
        print("当前时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("运行完..")

    def start_loop(self, loop):
        """
        再后台一直接受loop事件
        :param loop:
        :return:
        """
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def start_consume(self, ):
        """
        消费启动器， 负责把函数运行起来
        :return:
        """
        loop_thread = Thread(target=self.start_loop, args=(self.new_loop,))
        loop_thread.setDaemon(True)
        loop_thread.start()

        # save_loop_thread = Thread(target=self.start_loop, args=(self.save_loop,))
        # save_loop_thread.setDaemon(True)
        # save_loop_thread.start()

        save_data = Thread(target=self.before_save)
        save_data.setDaemon(True)
        save_data.start()

        self.consume()

    @abc.abstractmethod
    def start_produce(self):
        """首次生产函数， 以yield形式返回"""
        pass

    @abc.abstractmethod
    def parse(self, res):
        """请求之后解析函数"""
        pass

    async def request(self, message, channel, tag, properties):
        """
        请求函数，
        :param message: list 爬虫信息
        :param channel:
        :param tag:
        :param properties:
        :return:
        """
        logger.debug("开始请求url为：%s" % message["url"])
        message = middleware(message, auto_proxy=self.auto_proxy, auto_cookies=self.auto_cookies,
                             auto_headers=self.auto_headers)
        message = self.remessage(message)
        is_async = message.get("is_async", True)
        self.is_async = is_async
        verify = message.get("verify", False)
        cookies = message.get("cookies", {})
        if not cookies and self.cookies:
            cookies = self.cookies
        url = message.get("url", '')
        callback = message.get("callback", "parse")
        result = None
        if message["domain_name"] is None:
            if hasattr(self, callback):
                result = self.__getattribute__(callback)(message)
        else:
            if self._pre_domain_name != message["domain_name"] and message["domain_name"] is not None:
                if self.session:
                    tools.close_session(self.session)
                self.session = await tools.create_session(is_async, verify, cookies)
            self._pre_domain_name = message["domain_name"]
            res = await tools.request(url, self.session, message, auto_proxy=self.auto_proxy, allow_code=self.allow_code,
                                      is_async=is_async
                                      )
            if hasattr(self, callback):
                result = self.__getattribute__(callback)(res)
        if not result:
            channel.basic_ack(delivery_tag=tag.delivery_tag)
        else:
            if isinstance(result, dict):
                result["channel"] = channel
                result["tag"] = tag
                self._result_queue.put(result)
            elif isinstance(result, list):
                result.append(channel)
                result.append(tag)
                self._result_queue.put(result)
            else:
                logger.error("返回值必须是字典类型!")
                raise Exception()

    def remessage(self, message):
        """
        low版中间件
        :param message:
        :return:
        """
        return message

    def callback(self, channel, method, properties, body):
        """
        把请求函数传到异步事件中等待执行
        :param channel:
        :param method:
        :param properties:
        :param body:
        :return:
        """
        message = json.loads(body)
        future = asyncio.run_coroutine_threadsafe(self.request(message, channel, method, properties), self.new_loop)
        if future.exception():
            raise future.exception()

    async def save(self, mes, method, table_name, loop):
        """
        存储函数，负责吧爬下的数据存到mysql数据库中
        :return:
        """
        try:
            if method == "insql":
                await loop.run_in_executor(None, self.insql, table_name, mes)
            if method == "update":
                values = mes["values"]
                conditions = mes["conditions"]
                await loop.run_in_executor(None, self.update, table_name, values, conditions)
            if method == "delete":
                await loop.run_in_executor(None, self.delete, table_name, mes)
            if method == "select":
                pass
        except Exception:
            traceback.print_exc()
            os._exit(1)

    def before_save(self):
        try:
            while True:
                datas = self._result_queue.get()
                mess, tasks = [], []
                if isinstance(datas, dict):
                    channel = datas.pop("channel")
                    tag = datas.pop("tag")
                    mess.append(datas)
                elif isinstance(datas, list):
                    tag = datas.pop()
                    channel = datas.pop()
                    for data in datas:
                        if isinstance(data, dict):
                            mess.append(data)
                        else:
                            logger.error("返回值必须是dict")
                            raise Exception()
                else:
                    logger.error("返回值必须是dict")
                    raise Exception()
                channel.basic_ack(delivery_tag=tag.delivery_tag)
                for mes in mess:
                    table_name = mes.get("table_name", self.table_name)
                    if "table_name" in mes.keys():
                        table_name = mes.pop("table_name")
                        if not table_name:
                            table_name = self.table_name
                    if table_name not in self.tables:
                        self.save_loop.run_in_executor(None, self.Mysql.create_table, self.table_name, mes)
                        logger.warning("未填写表名，默认建立以脚本名为表名的表或者没有表")
                    method = mes.pop("method") if "method" in mes else "insql"
                    tasks.append(self.save(mes, method, table_name, self.save_loop))
                future = self.save_loop.run_until_complete(asyncio.wait(tasks))
                self._result_queue.task_done()
        except Exception:
            traceback.print_exc()
            os._exit(1)

    def early(self):
        """爬虫开始之前，需要运行的代码可以放在这个函数中"""
        pass