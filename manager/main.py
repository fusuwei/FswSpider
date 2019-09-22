from tools import request
import abc


class Spider:

    def __init__(self):
        pass

    def init(self):
        pass

    @abc.abstractmethod
    def start_spider(self):
        pass

    @abc.abstractmethod
    def parse(self):
        pass

    def producer(self):
        pass
