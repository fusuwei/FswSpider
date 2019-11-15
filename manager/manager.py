from tools import *
from queue import Queue
from inspect import isgeneratorfunction
from threading import Thread
import time
import abc
import asyncio
import setting
import json
import traceback
import functools
import os
logger = log(__name__)
PATH = setting.PATH


class Spider(metaclass=abc.ABCMeta):
    def __init__(self):
        # 爬虫脚本配置
        self.auto_proxy = False
        self.auto_cookies = False
        self.auto_headers = False
        self.clear_cookies = True
        self.allow_code = []
        self._url_md5 = set()
        self.is_async = True
        self.cookies = None
        self.max_times = 3
        self.timeout = 10
        self.download_delay = None
        self.session = None
        self.debug = False
        self.get_ip = False
        self.headers = None

        # 数据库配置
        self.mysql_host = None
        self.mysql_user = None
        self.mysql_pwd = None
        self.mysql_port = None
        self.dbname = None
        self.table_name = None
        self.mysqlconnecting = mysqlconnecting

        # RabbitMq配置
        self.rabbitmq_host = None
        self.rabbitmq_user = None
        self.rabbitmq_pwd = None
        self.is_purge = False

        self._pre_domain_name = None
        self._count_ = set()

    def init(self, spider_name=None):
        """
        初始化函数， mysql, RabbitMq 连接, 其他配置
        :return:
        """
        # 爬虫配置初始化
        if spider_name:
            self.spider_name = spider_name
            setting.spider_name = spider_name
        elif self.spider_name:
            setting.spider_name = self.spider_name
        elif setting.spider_name:
            self.spider_name = setting.spider_name
        else:
            logger.error("未配置爬虫名")
            raise ValueError("未配置爬虫名！")

        if self.async_number:
           setting.async_number = self.async_number
        elif setting.async_number:
            self.async_number = setting.async_number
        else:
            setting.async_number = self.async_number = 1

        # mysql连接
        self.Mysql, self.mysql_host, self.mysql_user, self.mysql_pwd, self.mysql_port \
            = mysqlconnecting(self.dbname, self.mysql_host, self.mysql_user, self.mysql_pwd, self.mysql_port)

        self.insql = self.Mysql.insql
        self.delete = self.Mysql.delete
        self.select = self.Mysql.select
        self.update = self.Mysql.update

        # rabbitmq连接
        self.Rabbit = rabbitconnecting(self.spider_name, self.rabbitmq_host, self.rabbitmq_user, self.rabbitmq_pwd)
        self.rabbitmq_host = self.Rabbit.rabbitmq_host
        self.rabbitmq_user = self.Rabbit.rabbitmq_user
        self.rabbitmq_pwd = self.Rabbit.rabbitmq_pwd

        # 其他参数
        self._produce_count = 1
        self.selector = selector
        self.new_loop = asyncio.new_event_loop()
        self.save_loop = asyncio.new_event_loop()

        self.item = Queue()
        self.Request = Request
        self.Response = Response
        self.Item = Item
        self.is_invalid = True
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

    @abc.abstractmethod
    def parse(self, res):
        pass

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

        save_thread = Thread(target=self.start_save, )
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
        while True:
            self.Rabbit.consume(callback=self.callback, prefetch_count=self.async_number)
            break

        print("---------------------------------------")
        self.item.join()
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
        if obj.count >= 3:
            if obj.count == 3:
                self._count_.add(get_md5(obj.to_publish()))
            if len(self._count_) == self.Rabbit.is_empty(self.spider_name, self.rabbitmq_host, self.rabbitmq_user, self.rabbitmq_pwd):
                logger.error("队列请求全部报错！")
                os._exit(1)
            obj.count += 1
            self.dispatch(obj, obj)
            channel.basic_ack(delivery_tag=tag)
        else:
            asyncio.run_coroutine_threadsafe(self.before_deal(obj, channel, tag), self.new_loop)

    async def before_deal(self, obj, channel, tag):
        try:
            res = await request(self, obj)
            time.sleep(0.003)
            if self._flag:
                self.item.join()
        except Exception:
            traceback.print_exc()
            os._exit(1)
        else:
            if res:
                self.dispatch(res, obj)
        finally:
            self.Rabbit.connection.add_callback_threadsafe(functools.partial(channel.basic_ack, delivery_tag=tag))

    def start_save(self,):
        tasks = []
        for i in range(1):
            tasks.append(before_save(self.item, self.table_name, self.Mysql, self.save_loop, self.sql_error))
        self.save_loop.run_until_complete(asyncio.wait(tasks))

    def sql_error(self):
        self._flag = True
        self._url_md5.clear()
        while True:
            item = self.item.get()
            self.produce(item.request)
            self.item.task_done()
            if self.item.empty():
                return