from spider import Spider
from manager.run import run


class MySpider(Spider):
    def __init__(self):
        super(MySpider, self).__init__()
        self.dbname = "test"
        self.table_name = "test"
        self.is_purge = True

    def start_produce(self):
        for i in ["https://www.baidu.com/s?wd=%E4%BE%8B%E5%AD%90", "https://www.baidu.com/", ]:
            yield {"url":i, "is_async":False}

    def parse(self, res):
        print(res.status_code)
        return {"content": res.status_code}


if __name__ == '__main__':
    run("test.py", function="w")

