from typing import *
import re
from tools.toolslib import get_cookies
from tools.proxy import get_ip, ip_process
from tools.user_agents import get_ua
from tools import log
logger = log(__name__)


class Request:
    def __init__(self, url: Union[int, str], method: str = "GET", callback: str = "parse",
                 data: Union[dict, None] = None, params: Union[dict, None] = None, json: Union[dict, None] = None,
                 headers: Union[dict, None] = None, proxies: str = None, timeout: Union[int, float] = 3,
                 max_times: int = 3, cookies: Union[dict, None] = None, verify: bool = False,
                 is_async: bool = True,  allow_redirects=False,):
        self.url = url
        self.method = method
        self.headers = headers
        self.callback = callback
        self.data = data
        self.params = params
        self.json = json
        self.proxies = proxies
        self.timeout = timeout
        self.max_times = max_times
        self.cookies = cookies
        self.verify = verify
        self.is_async = is_async
        self.allow_redirects = allow_redirects
        self.count = 0

    def to_dict(self):
        dic = {}
        for key in self.__dict__.keys():
            if self.__dict__[key]:
                dic[key] = self.__dict__[key]
        return dic

    def to_publish(self):
        dic = {}
        for key in self.__dict__.keys():
            if self.__dict__[key]:
                if key in ["url", "method", "callback", "data", "json", "params", "callback"]:
                    dic[key] = self.__dict__[key]
        return dic

    def auto_cookies(self, auto_proxy):
        if self.proxies:
            proxies = self.proxies.replace("http://", "").replace("https://", "")
            cookies = get_cookies(self.url, proxy=proxies)
        elif auto_proxy:
            proxies = get_ip()
            cookies = ''
            if proxies:
                proxies = proxies.replace("http://").replace("https://")
                cookies = get_cookies(self.url, proxy=proxies)
                self.proxies = proxies
        else:
            cookies = get_cookies(self.url)
        logger.debug("自动设置获取cookies为：%s" % cookies)
        self.cookies = cookies

    def auto_headers(self):
        headers = self.headers
        if headers:
            ua = get_ua()
            if "User-Agent" in headers:
                headers["User-Agent"] = ua
            elif "user-agent" in headers:
                headers["user-agent"] = ua
            else:
                headers["User-Agent"] = ua
            logger.debug("自动设置user-agent为：%s" % ua)
            self.headers = headers
        else:
            ua = get_ua()
            self.headers = {"User-Agent": ua}
            logger.debug("自动设置user-agent为：%s" % ua)

    def auto_proxy(self):
        proxies = get_ip()
        self.proxies = ip_process(proxies, self.is_async)
        logger.debug("更换ip为：%s" % proxies)
    @property
    def domain_name(self):
        return re.search("(http|https)://(www.)?(\w+(\.)?)+", self.url).group()