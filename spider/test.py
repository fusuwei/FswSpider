from spider import Spider
from manager.run import start


class MySpider(Spider):
    def __init__(self,):
        super(MySpider, self).__init__()
        self.is_purge = True
        self.init()

    def start_produce(self):
        for i in range(1):
            url = "https://www.baidu.com/"
            yield {"url": url}

    def parse(self, res):
        print(res.status_code)
        print()


if __name__ == '__main__':
    run = start()
    run(path='test.py', function="w")
