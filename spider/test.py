from manager import manager
from manager.runner import runner


class MySpider(manager.Spider):
    def __init__(self):
        super(MySpider, self).__init__()
        self.dbname = "test"
        self.table_name = "test"
        self.async_number = 1
        self.is_purge = True
        self.debug = "w"

    def start_produce(self):
        for i in ["https://www.baidu.com/s?wd=%E4%BE%8B%E5%AD%90", "https://www.baidu.com/", "https://fanyi.baidu.com/"]:
            yield self.Request(url=i,)

    def parse(self, res):
        print(res.status_code)
        return [self.Item(status_code=res.status_code+i) for i in range(1)]


if __name__ == '__main__':
    runner("test.py")

