from spider import Spider


class MySpider(Spider):
    def __init__(self,):
        super(MySpider, self).__init__()

    def start_produce(self):
        for i in range(2000):
            url = "https://www.baidu.com/"
            yield {"url": url}

    def parse(self, res):
        print(res.status_code)
        print()
