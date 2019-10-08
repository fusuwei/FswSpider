from spider import Spider
from manager.run import start


class MySpider(Spider):
    def __init__(self,):
        super(MySpider, self).__init__()
        self.dbname = "test"
        self.table_name = 'test'
        self.is_purge = True
        self.init(proxies=True)

    def start_produce(self):
        for i in range(2):
            url = "https://www.baidu.com/"
            yield {"url": url}

    def parse(self, res):
        print(res.status_code)
        self.produce({"url": "weqwewq"})
        self.insql("test", values=[0, res.text])


if __name__ == '__main__':
    # run = start()
    # run(path='test.py', function="w", async_number=1)
    import requests
    requests.get("https://www.baidu.com/", proxies={"http":""})