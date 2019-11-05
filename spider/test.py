from manager import manager
from manager.runner import run


class MySpider(manager.Spider):
    def __init__(self):
        super(MySpider, self).__init__()
        self.dbname = "test"
        self.table_name = "test"
        self.async_number = 1
        self.is_purge = True
        # self.auto_proxy = True
        self.debug = "w"

    def start_produce(self):
        for i in range(100):
            yield self.Request(url="https://www.baidu.com", )

    def parse(self, res):
        print(res.status_code)
        import time
        # print("1234")

        # return self.Item(content=res.status_code)


if __name__ == '__main__':
    run("spider\\test.py")
