from tools import req, get_ua, get_ip, get_cookies, log, RabbitMq, MySql, get_md5, ExceptErrorThread
import time
import re
import abc
import asyncio
import configparser
from importlib import import_module
from threading import Thread
import setting
import json
import random
import traceback
import sys
import os
logger = log(__name__)
PATH = setting.PATH


class Spider:
    def __init__(self):
        self._url_md5 = set()

        self.allow_code = []
        self._produce_count = 1

        self.async_number = None
        self.function = None
        self.spider_name = None
        self.is_purge = None

        self.table_name = None
        self.dbname = None

        self.is_create_sql = setting.is_create_sql

    def init(self, proxies=False, cookies=False, headers=True):
        async_number = self.__getattribute__('async_number')
        if not async_number:
            self.async_number = setting.async_number
        function = self.__getattribute__('function')
        if not function:
            self.function = setting.function

        spider_name = self.__getattribute__('spider_name')
        if not spider_name:
            self.spider_name = setting.spider_name

        is_purge = self.__getattribute__('is_purge')
        if not is_purge:
            self.is_purge = setting.is_purge

        self.proxies = proxies
        self.cookies = cookies
        self.headers = headers
        self.rabbit = RabbitMq.connect(self.spider_name)
        if self.is_create_sql:
            self.mysql = MySql.mysql_pool()
            self.mysql.create_db()
        else:
            self.mysql = MySql.mysql_pool(self.dbname)

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    @abc.abstractmethod
    def start_produce(self):
        """首次生产函数， 以yield形式返回"""
        pass

    @abc.abstractmethod
    def parse(self, res):
        """请求之后解析函数"""
        pass

    async def request(self, message, channel, tag, properties):
        try:
            logger.debug("开始请求url为：%s" % message["url"])
            message = self.pretreatment(message)
            message = self.remessage(message)
            url = message.get("url", None)
            callback = message.get("callback", "parse")
            max_times = message.get("max_times", 3)
            method = message.get("method", "GET")
            data = message.get("data", None)
            params = message.get("params", None)
            headers = message.get("headers", None)
            proxies = message.get("proxies", None)
            timeout = message.get("timeout", None)
            json = message.get("json", None)
            cookies = message.get("cookies", None)
            allow_redirects = message.get("allow_redirects", False)
            verify_ssl = message.get("verify_ssl", False)
            limit = message.get("limit", 100)
            res = None
            if url and "http" in url:
                for i in range(1, max_times + 1):
                    res = await req.request(url=url, method=method, data=data, params=params, headers=headers,
                                            proxies=proxies, timeout=timeout, json=json, cookies=cookies,
                                            allow_redirects=allow_redirects, verify_ssl=verify_ssl, limit=limit)
                    if res.status_code != 200 and res.status_code is not None:
                        logger.warning("第%d次请求！状态码为%s" % (i, res.status_code))
                        if res.status_code in self.allow_code:
                            break
                    else:
                        break
                if callback and hasattr(self, callback):
                    self.__getattribute__(callback)(res)
                    channel.basic_ack(delivery_tag=tag.delivery_tag)
                else:
                    raise ValueError("必须构建回调函数")
            else:
                if callback and hasattr(self, callback):
                    self.__getattribute__(callback)(message)
                    channel.basic_ack(delivery_tag=tag.delivery_tag)
        except Exception:
            ex_type, ex_val, ex_stack = sys.exc_info()
            logger.error(ex_type)
            logger.error(ex_val)
            for stack in traceback.extract_tb(ex_stack):
                logger.error(stack)
            os._exit(-1)

    def pretreatment(self, message):
        if self.headers:
            headers = message.get("headers", get_ua())
            if isinstance(headers, dict):
                ua = get_ua()
                logger.debug("自动设置user-agent为：%s" % headers)
                headers["User-Agent"] = ua
                message["headers"] = headers
            else:
                logger.debug("自动设置user-agent为：%s" % headers)
                message["headers"] = {"User-Agent": headers}
        if self.proxies:
            proxies = message.get("proxies", get_ip())
            logger.debug("自动设置代理ip为：%s" % proxies)
            message["proxies"] = proxies
        else:
            proxies = message.get("proxies", "")
            if proxies and isinstance(proxies, str) and "http" not in proxies:
                proxies = "http://"+proxies
            elif proxies and (isinstance(proxies, list) or isinstance(proxies, tuple)):
                proxy = random.choice(proxies)
                if "http" not in proxy:
                    proxies = "http://" + proxy
                else:
                    proxies = proxy
            elif proxies and isinstance(proxies, dict):
                proxy = random.choice(list(proxies.values()))
                if "http" not in proxy:
                    proxies = "http://" + proxy
                else:
                    proxies = proxy
            message["proxies"] = proxies
        if self.cookies:
            cookies = message.get("cookies", get_cookies())
            logger.debug("自动设置获取cookies为：%s" % cookies)
            message["cookies"] = cookies
        return message

    def remessage(self, message):
        return message

    def produce(self, message=None, if_empty=False):
        logger.debug("开始生产！")
        if self.function == "m":
            if hasattr(self, "start_produce"):
                start_produce = getattr(self, "start_produce")
                if not self.rabbit.queue.method.message_count or not self.is_purge:
                    pass
                elif self.is_purge:
                    self.rabbit.purge(self.spider_name)
                for i, message in enumerate(start_produce()):
                    md5 = get_md5([message.get("url", ""), message.get("data", '')])
                    if md5 not in self._url_md5:
                        print("[%d]生产：" % (i+1), message)
                        message = json.dumps(message)
                        self.rabbit.pulish(message)
                        self._url_md5.add(md5)

        elif self.function == "w":
            md5 = get_md5([message.get("url", ""), message.get("data", '')])
            if md5 not in self._url_md5:
                print("[%d]生产：" % (self._produce_count + 1), message)
                message = json.dumps(message)
                self.rabbit.pulish(message)

    def listen(self):
        pass

    def consume(self):
        # heartbeat = Heartbeat(self.rabbit.connection)  # 实例化一个心跳类
        # heartbeat.start()  # 开启一个心跳线程，不传target的值默认运行run函数
        # heartbeat.startheartbeat()  # 开启心跳保护
        self.rabbit.consume(callback=self.callback, limit=self.async_number)
        self.rabbit.del_queue(self.spider_name)
        print("当前时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("运行完..")

    def callback(self, channel, method, properties, body):
        message = json.loads(body)
        asyncio.run_coroutine_threadsafe(self.request(message, channel, method, properties), self.new_loop)

    def insql(self, tablename, keys=None, values=None, items=None):
        # print(keys, values, items)
        if keys and not isinstance(keys, list):
            logger.error("keys 必须是 list")
            raise ValueError()
        if values and not isinstance(values, list):
            logger.error("values 必须是 list")
            raise ValueError()
        if items and not isinstance(values, dict):
            logger.error("items 必须是 dict")
            raise ValueError()
        if keys and values and not len(keys) != len(values):
            logger.error("keys 和 values 不一样长")
            raise ValueError()
        # ty = lambda x: "'%s'" % x if isinstance(x, str) or "str" in str(type(x)) or "Str" in str(type(x)) else x
        # if values:
        #     values = [ty(i) for i in values]
        # if items:
        #     for k, v in items.items():
        #         items[k] = ty(v)
        self.mysql.insql(tablename, keys, values, items)

    def delete(self, tablename, key, value):
        self.mysql.delete(tablename, key, value,)

    def select(self, tablename, key=None, value=None, v="*", term=None, one=False):
        self.mysql.select(tablename, key, value, v, term, one)

    def run(self,):
        self.new_loop = asyncio.new_event_loop()

        loop_thread = Thread(target=self.start_loop, args=(self.new_loop,))
        loop_thread.setDaemon(True)
        loop_thread.start()

        self.consume()


def runner(path=None, function=None, spider_name=None, async_number=None):

    if not path and not function:
        cfg = configparser.ConfigParser()
        cfg.read(PATH + "\manager\_spider.cfg", encoding="utf8")
        path = cfg.get('spider', 'path')
        function = cfg.get('spider', 'function')
        spider_name = cfg.get('spider', 'spider_name', fallback='')
        async_number = cfg.get('spider', 'async_number', fallback=1)

        keys = [key for key in cfg.keys()]
        if "create db" in keys and "create table" in keys:
            db_dict, tb_dict = {}, {}
            for key, val in cfg.items("create db"):
                db_dict[key] = val

            for key, val in cfg.items("create table"):
                tb_dict[key] = val
            setting.db_dict = db_dict
            setting.tb_dict = tb_dict

    if async_number:
        setting.async_number = async_number
    if function:
        setting.function = function
    if spider_name:
        setting.spider_name = spider_name
    else:
        if path:
            spider_name = re.search("([0-9a-zA-Z]+)\.py", path).group(1)
            setting.spider_name = spider_name
        else:
            raise ValueError("必须指定路径！")

    if path and path.endswith(".py"):
        path = "spider." + path.replace("/", '.').strip(".py")

        spider_cls = import_module(path, "MySpider")
        spider = spider_cls.MySpider()
        if function == "m":
            spider.produce()
        elif function == "w":
            spider.run()
