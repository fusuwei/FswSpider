from tools.user_agents import get_ua
from tools.proxy import get_ip, ip_process
from tools.toolslib import get_cookies
from tools.wangyiyidun import CrackSlider
import random
import json


class DefaultMiddleware:
    def process_request(self, request, spider):
        if spider.auto_headers:
            request.headers = {"User-Agent": get_ua()}
        if spider.auto_proxy:
            mysql = spider.MySql.mysql_pool(dbname="proxypool", mysql_host="127.0.0.1", mysql_user="root", mysql_pwd="123456")
            proxies = get_ip(mysql)
            request.proxies = ip_process(proxies, spider.is_async)
        if spider.auto_cookies:
            if spider.is_invalid:
                if request.proxies:
                    proxies = request.proxies.replace("http://", "").replace("https://", "")
                    cookies = get_cookies(request.domain_name, proxy=proxies)
                else:
                    cookies = get_cookies(request.domain_name)
                request.cookies = cookies
        return request, spider


class WangYiYunBuff:
    def __init__(self):
        self.crackSlider = CrackSlider
        self.cookies = None

    def process_request(self, request, spider):
        if not self.cookies:
            self.cookies = spider.Mysql.select("cookies", ["*"], {"id": random.randint(1, 7)})[0]
        if spider.is_invalid:
            phone = self.cookies["phone"]
            pwd = self.cookies["pwd"]
            c = self.crackSlider()
            while True:
                try:
                    request.cookies = c.crack_slider(phone, pwd)
                    c.close()
                except Exception:
                    c.close()
                    continue
                else:
                    break
            spider.Mysql.update("cookies", {"cook": request.cookies}, {"phone": phone})
        else:
            self.cookies = spider.Mysql.select("cookies", ["*"], {"id": random.randint(1, 7)})[0]
            if self.cookies["cook"]:
                request.cookies = json.loads(self.cookies["cook"].replace("'", '"'))
            else:
                request.cookies = None
        return request, spider


class LaGouWang:
    def process_request(self, request, spider):
        if spider.is_invalid:
            cookies = get_cookies(request.domain_name)
            request.cookies = cookies
        request.headers = {
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        }
        return request, spider