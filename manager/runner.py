import setting
import re
from importlib import import_module


def runner(path=None, is_auto=False):

    if path and path.endswith(".py"):
        spider_name = re.search("([0-9a-zA-Z]+)\.py", path).group(1)
        setting.spider_name = spider_name

        path = path.replace("\\", '/')
        if "spider" in path:
            path = path.replace("/", '.').strip(".py")
        else:
            path = "spider." + path.replace("/", '.').strip(".py")

        spider_cls = import_module(path, "MySpider")
        spider = spider_cls.MySpider()
        spider.init(spider_name, path, is_auto)
        if hasattr(spider, "early"):
            spider.early()
        spider.start()


def run(path, is_auto=False):
    runner(path=path, is_auto=is_auto)