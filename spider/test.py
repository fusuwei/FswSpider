from manager import manager
from manager.runner import run


class MySpider(manager.Spider):
    def __init__(self):
        super(MySpider, self).__init__()
        self.dbname = "test"
        self.table_name = "test"
        self.async_number = 1
        self.is_purge = True
        self.debug = False

    def start_produce(self):
        for i in ["https://www.google.com/"]:
            yield self.Request(url=i,)

    def parse(self, res):
        print(res.status_code)
        return [self.Item(content=res.status_code+i) for i in range(10)]


if __name__ == '__main__':
    run("spider\\test.py")

