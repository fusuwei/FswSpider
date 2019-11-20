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
    # run("spider\\test.py")
    import requests

    headers = {
        'cookie': 'api_uid=rBUGXl13BJMCpnbd9sQUAg==; JSESSIONID=EDBE9CA5F7297DF9F5058AB054241829',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    }
    content = '0anAfxnUdyhYY9TVZADYsDZ9BATYtI4t27s7HmWkNnkx4UBwgZsktwg7txyhEFujLs5DjZ_giG4Wi0QCFYstuxJqtnNbK8w_nH29QTp71fuZt0pCrLpqoZlz5Pg5y1cgl4zQa2mOhos77TM-VPsMwbtbLN5PmI7ZIfFxY7tS8dVVYzcyfavEAa7hsbMTSbsMI8e1bwh6m-5U1yGTxKbKcwA_dQh8Ixv7s7xIGk3z-OmtFF0xpXU1JjNjBiS1N4fUySdyWkhxIFoJUPmQ6ywHp4NFazWrrSRkfvsLkVL7DPsNbmHbrJRfaNjUrVw4vgn7qzSQO9HTUxZd5iJzTyb7CXrwsMmVuL5GVaRVyldrBA3wCA3jF_1BkKOBtRjUbKK-Kp4XE10GKo9QgubV1XoZCPxnYGpJQn9bxa1yCr4YqEHXoaO9CRTtcoHBiaECxlYkDLU47a0CFW5EKuUBvXX-A0insFBavjnIxuEfptboPYoNTcrXWdqLfeFa1mrB4v4XpT1kxDc5qbXaKRlmekU6GRMEv1mJkcJtMtcdgH-H-Ep7DEKh-sqvZ7LtpV6jLSRtxnIOF1oBWgiqHIfDzDLSx-L87FKhDVjwJ6jbAOJ-BLAnA-yilRY6b0wOMS'
    ret = requests.get("http://apiv3.yangkeduo.com/search?source=search&search_met=hot&track_data=refer_page_id,10015_1574238006017_bSqBemslRS;refer_search_met_pos,1&list_id=oxtDtkoY8l&sort=default&filter=&q=%E7%94%B7%E6%AC%BE%E7%9D%A1%E8%A1%A3%E7%A7%8B%E5%86%AC&page=2&size=50&flip=20;5;0;0;53bed434-965d-47fe-baa7-97b6098a36c3&anti_content={}&pdduid=0".format(content),
                       headers=headers, allow_redirects=False)
    ret.cookies.get_dict()
    print(ret)