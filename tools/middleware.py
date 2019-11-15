from tools.user_agents import get_ua
from tools.proxy import get_ip, ip_process
from tools.toolslib import get_cookies
from tools.wangyiyidun import CrackSlider
import random
import json
import setting


class DefaultMiddleware:
    def process_request(self, request, spider):
        if spider.get_ip:
            mysql = spider.mysqlconnecting(dbname="proxypool", mysql_host="127.0.0.1", mysql_user="root", mysql_pwd="123456")[0]
            get_ip(mysql)
            spider.get_ip = False
        if spider.auto_headers:
            request.headers = {"User-Agent": get_ua()}
        if spider.clear_cookies:
            if spider.is_async:
                spider.session.cookie_jar.clear()
            else:
                spider.session.cookies.clear()
        if spider.auto_proxy:
            if setting.proxies:
                proxies = random.choice(setting.proxies)
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


# class WangYiYunBuff:
#     def __init__(self):
#         self.crackSlider = CrackSlider
#         self.cookies = None
#
#     def process_request(self, request, spider):
#         if not self.cookies:
#             self.cookies = spider.Mysql.select("cookies", ["*"], {"id": random.randint(1, 7)})[0]
#         if spider.is_invalid:
#             phone = self.cookies["phone"]
#             pwd = self.cookies["pwd"]
#             c = self.crackSlider()
#             while True:
#                 try:
#                     request.cookies = c.crack_slider(phone, pwd)
#                     c.close()
#                 except Exception:
#                     c.close()
#                     continue
#                 else:
#                     break
#             spider.Mysql.update("cookies", {"cook": request.cookies}, {"phone": phone})
#         else:
#             self.cookies = spider.Mysql.select("cookies", ["*"], {"id": random.randint(1, 7)})[0]
#             if self.cookies["cook"]:
#                 request.cookies = json.loads(self.cookies["cook"].replace("'", '"'))
#             else:
#                 request.cookies = None
#         return request, spider


class LaGouWang:
    def __init__(self):
        self._count = 0

    def process_request(self, request, spider):
        if "show=" in request.url:
            if setting.proxies:
                proxies = random.choice(setting.proxies)
                request.proxies = ip_process(proxies, spider.is_async)
            request.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            }
            return request, spider

        elif spider.is_invalid:
            if setting.proxies:
                proxies = random.choice(setting.proxies)
                request.proxies = ip_process(proxies, spider.is_async)
            cookies = get_cookies(request.domain_name, proxy=request.proxies)
            request.cookies = cookies
            request.headers = {
                'Host': 'www.lagou.com',
                'Origin': 'https://www.lagou.com',
                'Referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            }
            self._count += 1
            return request, spider
        else:
            return request, spider


class BossZhiPin:
    def process_request(self, request, spider):
        if not spider.headers:
            spider.headers = {
                'sec-fetch-mode':'navigate',
                'sec-fetch-site':'same-origin',
                'sec-fetch-user':'?1',
                'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            }
        request.allow_redirects = False
        request.headers = spider.headers
        return request, spider