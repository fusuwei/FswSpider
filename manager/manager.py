from tools import *
from tools.proxy import ip_process
from queue import Queue
from inspect import isgeneratorfunction
from threading import Thread
from concurrent.futures import Future
import time
import abc
import asyncio
import setting
import json
import traceback
import os
logger = log(__name__)
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
        self.debug = False

        # 数据库配置
        self.mysql_host = "127.0.0.1"
        self.mysql_user = "root"
        self.mysql_pwd = ""
        self.mysql_port = 3306
        self.dbname = "FswSpider"
        self.table_name = ""

        # RabbitMq配置
        self.rabbitmq_host = "127.0.0.1"
        self.rabbitmq_user = "fsw"
        self.rabbitmq_pwd = ""
        self.is_purge = False

        self._pre_domain_name = None

        self._result_queue = Queue()
        self._request_ls = list()

    def init(self):
        """
        初始化函数， mysql, RabbitMq 连接, 其他配置
        :return:
        """
        # 爬虫配置初始化
        self.spider_name = setting.spider_name
        if not self.spider_name:
            pass

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
            self.Mysql = MySql.mysql_pool(dbname=self.dbname, mysql_host=self.mysql_host, mysql_port=self.mysql_port,
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
            logger.error("请配置数据库参数")
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
            self.Rabbit = RabbitMq.connect(self.spider_name, rabbitmq_host=self.rabbitmq_host,
                                           rabbitmq_user=self.rabbitmq_user, rabbitmq_pwd=self.rabbitmq_pwd)

        # 其他参数
        self._produce_count = 1
        self.selector = selector
        self.new_loop = asyncio.new_event_loop()
        self.save_loop = asyncio.new_event_loop()

        self.item = Queue()
        self.Request = Request
        self.Response = Response
        self.Item = Item

        self._flag = False

    def start(self):
        if not self.debug or (self.debug and self.debug == 'm'):
            if self.is_purge:
                self.Rabbit.purge(self.spider_name)
            if hasattr(self, "start_produce"):
                if isgeneratorfunction(self.start_produce):
                    for obj in self.start_produce():
                        self.dispatch(obj)
                else:
                    objs = self.start_produce()
                    self.dispatch(objs)

        if not self.debug or (self.debug and self.debug == 'w'):
            self.start_consume()

    @abc.abstractmethod
    def start_produce(self):
        """
        首次运行spider
        :return:
        """
        pass

    def produce(self, obj=None):
        logger.debug("开始生产！")
        message = obj.to_publish()
        md5 = get_md5(message)
        if md5 not in self._url_md5:
            message = json.dumps(message)
            self.Rabbit.pulish(message)
            print("[%d]生产：" % (self._produce_count), message)
            self._url_md5.add(md5)
            self._produce_count += 1

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

        save_thread = Thread(target=self.start_save)
        save_thread.setDaemon(True)
        save_thread.start()

        self.consume()

    def dispatch(self, obj, obj2=None):
        if isinstance(obj, list) or isinstance(obj, tuple):
            for o in obj:
                if isinstance(o, self.Request):
                    self.produce(o)
                elif isinstance(o, self.Response):
                    ret = self.__getattribute__(o.callback)(obj)
                    self.dispatch(ret)
                elif isinstance(o, self.Item):
                    o.request = obj2
                    self.item.put(o)
        elif isinstance(obj, self.Request):
            self.produce(obj)
        elif isinstance(obj, self.Response):
            ret = self.__getattribute__(obj.callback)(obj)
            self.dispatch(ret)
        elif isinstance(obj, self.Item):
            obj.request = obj2
            self.item.put(obj)

    def consume(self):
        """
        消费函数
        :return:
        """
        # heartbeat = Heartbeat(self.rabbit.connection)  # 实例化一个心跳类
        # heartbeat.start()  # 开启一个心跳线程，不传target的值默认运行run函数
        # heartbeat.startheartbeat()  # 开启心跳保护
        self.Rabbit.consume(callback=self.callback, limit=self.async_number, item_queue=self.item)
        print("---------------------------------------")
        self.Rabbit.del_queue(self.spider_name)
        print("当前时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("运行完..")

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
        tag = method.delivery_tag
        obj = Request(**message)
        future = asyncio.run_coroutine_threadsafe(self.request(obj, channel, tag), self.new_loop)
        try:
            res = future.result()
            if self._flag:
                self.item.join()
        except Exception:
            traceback.print_exc()
            os._exit(1)
        else:
            self.dispatch(res, obj)
            channel.basic_ack(delivery_tag=tag)

    async def request(self, obj, channel, tag):
        """
        请求函数，
        :param message: list 爬虫信息
        :param channel:
        :param tag:
        :param properties:
        :return:
        """
        res = None
        while obj.max_times:
            obj.max_times -= 1
            callback = self.__getattribute__(obj.callback)
            self.is_async = obj.is_async
            if hasattr(obj, "err"):
                err = getattr(obj, "err")
            if self.auto_cookies and not self.cookies:
                obj.auto_cookies(self.auto_proxy)
                self.cookies = obj.cookies
            if self.auto_headers:
                obj.auto_headers()
            if self.auto_proxy:
                obj.auto_proxy()
            logger.debug("开始请求url为：%s" % obj.url)
            obj = self.remessage(obj)
            if obj.proxies:
                obj.proxies = ip_process(obj.proxies, obj.is_async)
            if not obj.domain_name:
                ret = callback(obj)
                return ret
            else:
                if self._pre_domain_name != obj.domain_name and obj.domain_name is not None:
                    if self.session:
                        await close_session(session=self.session)
                    self.session = await create_session(obj.is_async, obj.verify, obj.cookies)
                self._pre_domain_name = obj.domain_name
                res = await request(self.session, obj, self.Response, auto_proxy=self.auto_proxy, allow_code=self.allow_code)
                if isinstance(res, self.Request):
                    continue
                else:
                    ret = callback(res)
                    return ret
        self.produce(res)
        channel.basic_ack(delivery_tag=tag)

    def remessage(self, message):
            """
            low版中间件
            :param message:
            :return:
            """
            return message

    async def save(self, mes, method, table_name, loop):
        """
        存储函数，负责吧爬下的数据存到mysql数据库中
        :return:
        """
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

    async def before_save(self, item):
        if item.table_name:
            table_name = item.table_name
        elif self.table_name:
            table_name = self.table_name
        else:
            logger.error("请配置table_name!")
            raise Exception()
        data = item.to_dict()
        if table_name not in self.tables:
            self.save_loop.run_in_executor(None, self.Mysql.create_table, self.table_name, data)
            logger.warning("未填写表名，默认建立以脚本名为表名的表或者没有表")
        method = item.method
        await self.save(data, method, table_name, self.save_loop)
        return 1

    def start_save(self):
        while True:
            item = self.item.get()
            try:
                future = self.save_loop.run_until_complete(self.before_save(item))
                if future:
                    self.item.task_done()
            except Exception as e:
                self._flag = True
                while True:
                    item = self.item.get()
                    self.produce(item.request)
                    self.item.task_done()
                    if self.item.empty():
                        traceback.print_exc()
                        os._exit(1)