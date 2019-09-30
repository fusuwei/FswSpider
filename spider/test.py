from spider import Spider
from manager.run import start


class MySpider(Spider):
    def __init__(self,):
        super(MySpider, self).__init__()
        self.dbname = "test"
        self.table_name = 'test'
        self.is_purge = True
        self.init()

    def start_produce(self):
        for i in range(10):
            url = "https://www.baidu.com/"
            yield {"url": url}

    def parse(self, res):
        print(res.status_code)
        self.insql("test", values=[0, res.text])


if __name__ == '__main__':
    run = start()
    run(path='test.py', function="w", async_number=1)
