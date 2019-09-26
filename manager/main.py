import time
from tools import req, get_ua, get_ip, get_cookies, log, RabbitMq, Heartbeat
import abc
import asyncio
import configparser
from importlib import import_module
from queue import Queue
from threading import Thread
import setting
import json


PATH = setting.PATH


class Spider:
    def __init__(self):
        self.queue = Queue()
        self.async_number = setting.async_number
        self.function = setting.function
        self.spider_name = setting.spider_name
        self.proxies = False
        self.cookies = False
        self.headers = True
        self.allow_code = []
        self.rabbit = RabbitMq.connect(self.spider_name)
        self.logger = log(__name__)
        self._produce_count = 1

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    @abc.abstractmethod
    def start_produce(self):
        pass

    @abc.abstractmethod
    def parse(self, res):
        pass

    async def request(self, message, channel, tag, properties):
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
        for i in range(1, max_times + 1):
            res = await req.request(url=url, method=method, data=data, params=params, headers=headers,
                                    proxies=proxies, timeout=timeout, json=json, cookies=cookies,
                                    allow_redirects=allow_redirects, verify_ssl=verify_ssl, limit=limit)
            if res.status_code != 200 and res.status_code is not None:
                self.logger.warning("第%d次请求！状态码为%s" % (i, res.status_code))
                if res.status_code in self.allow_code:
                    break
            else:
                break
        if callback and hasattr(self, callback):
            self.__getattribute__(callback)(res)
            channel.basic_ack(delivery_tag=tag.delivery_tag)
        else:
            raise ValueError("必须构建回调函数")

    def pretreatment(self, message):
        if self.headers:
            headers = message.get("headers", get_ua())
            message["headers"] ={"User-Agent" :headers}
        if self.proxies:
            proxies = message.get("proxies", get_ip())
            message["proxies"] = proxies
        if self.cookies:
            cookies = message.get("cookies", get_cookies())
            message["cookies"] = cookies
        return message

    def remessage(self, message):
        return message

    def produce(self, message=None):
        if self.function == "m":
            if hasattr(self, "start_produce"):
                start_produce = getattr(self, "start_produce")
                for i,message in enumerate(start_produce()):
                    print("[%d]生产：" % (i+1), message)
                    message = json.dumps(message)
                    self.rabbit.pulish(message)
        elif self.function == "w":
            print("[%d]生产：" % (self._produce_count + 1), message)
            message = json.dumps(message)
            self.rabbit.pulish(message)

    def listen(self):
        pass

    def consume(self):
        heartbeat = Heartbeat(self.rabbit.connection)  # 实例化一个心跳类
        heartbeat.start()  # 开启一个心跳线程，不传target的值默认运行run函数
        heartbeat.startheartbeat()  # 开启心跳保护
        self.rabbit.consume(callback=self.callback, limit=self.async_number)

    def callback(self, channel, method, properties, body):
        message = json.loads(body)
        asyncio.run_coroutine_threadsafe(self.request(message, channel, method, properties), self.new_loop)

    def run(self,):

        self.new_loop = asyncio.new_event_loop()

        loop_thread = Thread(target=self.start_loop, args=(self.new_loop,))
        loop_thread.setDaemon(True)
        loop_thread.start()

        self.consume()


def runner():

    cfg = configparser.ConfigParser()
    cfg.read(PATH + "\manager\_spider.cfg")
    path = cfg.get('spider', 'path')
    function = cfg.get('spider', 'function')
    spider_name = cfg.get('spider', 'spider_name')
    async_number = cfg.get('spider', 'async_number', fallback='')
    if async_number:
        setting.async_number = async_number
    if function:
        setting.function = function
    if spider_name:
        setting.spider_name = spider_name

    if path and path.endswith(".py"):
        path = "spider." + path.replace("/", '.').strip(".py")

        spider_cls = import_module(path, "MySpider")
        spider = spider_cls.MySpider()
        if function == "m":
            spider.produce()
        else:
            spider.run()


