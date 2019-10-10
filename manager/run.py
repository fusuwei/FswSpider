import setting
import re
from importlib import import_module


def run(path=None, function=None, spider_name=None, async_number=None):

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
        path = path.replace("\\", '/')
        path = "spider." + path.replace("/", '.').strip(".py")

        spider_cls = import_module(path, "MySpider")
        spider = spider_cls.MySpider()
        spider.init()
        if function == "m":
            spider.produce()
        elif function == "w":
            spider.start_consume()

if __name__ == '__main__':
    run("text.py")