from spider import Spider


class MySpider(Spider):
    def __init__(self,):
        super(MySpider, self).__init__()

    def start_produce(self):
        for i in range(1):
            url = "https://www.baidu.com/"
            yield {"url": url}

    def parse(self, res):
        print()
        pass


import requests
if __name__ == '__main__':
    ret = requests.get("http://ecp.sgcc.com.cn", headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
            })
    print(ret.cookies.get_dict())