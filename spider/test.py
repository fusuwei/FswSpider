from manager import manager
from manager.runner import run


class MySpider(manager.Spider):
    def __init__(self):
        super(MySpider, self).__init__()
        self.dbname = "spider_auto_update"
        self.table_name = "test"
        self.async_number = 1
        self.is_purge = True
        self.download_delay = 0
        self.auto_update = 1
        self.update_freq = 0.01
        # self.timeout = 1
        # self.auto_proxy = True
        self.debug = "m"
        self.count = 1

    def start_produce(self):
        for i in range(10):
            yield self.Request(url="https://www.baidu.com", data={"1": i})

    def parse(self, res):
        self.count += 1
        return self.Request(url="https://www.baidu.com", callback="aaaa", data={"1": self.count})
        # print("1234")

    def aaaa(self, res):
        print(res.status_code)


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