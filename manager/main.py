import abc
import asyncio
import configparser
from importlib import import_module
from queue import Queue
from threading import Thread
import setting
from tools import request

PATH = setting.PATH


class Spider:
    def __init__(self):
        self.queue = Queue()
        self.async_number = setting.async_number

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    @abc.abstractmethod
    def start_produce(self):
        pass

    @abc.abstractmethod
    def parse(self):
        pass

    async def request(self, url=None, method="GET", data=None, params=None, headers=None, proxies=None, timeout=10,
            json=None, cookies=None,allow_redirects=False, verify_ssl=False, limit=100):
        ret = await  request.request(url)

        print()

    def produce(self):
        if hasattr(self, "start_produce"):
            start_produce = getattr(self, "start_produce")
            for message in start_produce():
                self.queue.put(message)

    def listen(self):
        pass

    def start(self):
        while True:
            message = self.queue.get()
            url = message['url']
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
            }
            asyncio.run_coroutine_threadsafe(self.request(url, headers=headers), self.new_loop)

    def run(self,):

        self.new_loop = asyncio.new_event_loop()

        loop_thread = Thread(target=self.start_loop, args=(self.new_loop,))
        loop_thread.setDaemon(True)
        loop_thread.start()

        loop_start = Thread(target=self.start)
        loop_start.setDaemon(True)
        loop_start.start()

        self.queue.join()


def runner():
    cfg = configparser.ConfigParser()
    cfg.read(PATH + "\manager\_spider.cfg")
    path = cfg.get('spider', 'path')
    function = cfg.get('spider', 'function')
    async_number = cfg.get('spider', 'async_number', fallback='')
    if async_number:
        setting.async_number = async_number

    if path and path.endswith(".py"):
        path = "spider." + path.replace("/", '.').strip(".py")

        spider_cls = import_module(path, "MySpider")
        spider = spider_cls.MySpider()
        # if function == "m":
        spider.produce()
        # else:
        spider.run()