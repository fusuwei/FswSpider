from spider import Spider
from manager.run import run


class MySpider(Spider):
    def __init__(self,):
        super(MySpider, self).__init__()
        self.dbname = "test"
        self.table_name = 'test'
        self.is_purge = True

    def start_produce(self):
        for i in range(2):
            url = "https://www.baidu.com/"
            yield {"url": url}

    def parse(self, res):
        print(res.status_code)
        return {"content": str(res.status_code)}


if __name__ == '__main__':
    run(path='test.py', function="w", async_number=1)
