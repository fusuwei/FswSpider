from spider import Spider


class MySpider(Spider):
    def __init__(self,):
        super(MySpider, self).__init__()

    def start_produce(self):
        for i in range(10):
            url = "http://ecp.sgcc.com.cn"
            yield {"url": url}

    def paese(self):
        pass


import requests
if __name__ == '__main__':
    ret = requests.get("http://ecp.sgcc.com.cn", headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
            })
    print(ret.cookies.get_dict())