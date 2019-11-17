from manager import manager
from manager.runner import run


class MySpider(manager.Spider):
    def __init__(self):
        super(MySpider, self).__init__()
        self.dbname = "test"
        self.table_name = "test"
        self.async_number = 10
        self.is_purge = True
        # self.auto_proxy = True
        self.debug = "w"

    def start_produce(self):
        for i in range(100):
            yield self.Request(url="https://www.baidu.com", timeout=1)

    def parse(self, res):
        print(res.status_code)
        import time
        time.sleep(10)
        # print("1234")

        # return self.Item(content=res.status_code)


if __name__ == '__main__':
    run("spider\\test.py")
    # import requests
    #
    # headers = {
    #     'sec-fetch-mode': 'navigate',
    #     'sec-fetch-site': 'same-origin',
    #     'sec-fetch-user': '?1',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    # }
    # ret = requests.get("https://www.zhipin.com/c100010000/?query=%E7%88%AC%E8%99%AB&page=2&ka=page-2",
    #                    headers=headers, allow_redirects=False)
    # print(ret)