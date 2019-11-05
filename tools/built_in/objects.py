import chardet
from typing import *
import re
from tools import log
from tools.toolslib import selector
logger = log(__name__)


class Response:
    def __init__(self, url, content=None, status_code=None, charset=None, cookies=None, method=None,
                 headers=None, callback="parse", proxies=None, error=None, meta=None):
        self.url = url
        self.content = content
        self.status_code = status_code
        self.charset = charset
        self.cookies = cookies
        self.method = method
        self.headers = headers
        self.callback = callback
        self.proxies = proxies
        self.error = error
        self.meta = meta
        self.text = self._parse_content(charset, content)
        self.resp = self.selector()

    def _parse_content(self, charset, content):
        if not content:
            return
        if charset:
            try:
                text = content.decode(charset)
            except UnicodeDecodeError:
                try:
                    char = chardet.detect(content)
                    if char:
                        text = content.decode(char)
                    else:
                        raise UnicodeDecodeError
                except UnicodeDecodeError:
                    try:
                        text = content.decode('utf-8')
                    except UnicodeDecodeError:
                        try:
                            text = content.decode("GBK")
                        except UnicodeDecodeError:
                            text = content.decode('utf-8', "ignore")
        else:
            try:
                text = content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    char = chardet.detect(content)
                    if char:
                        text = content.decode(char)
                    else:
                        raise UnicodeDecodeError
                except UnicodeDecodeError:
                    try:
                        text = content.decode('gb2312')
                    except UnicodeDecodeError:
                        text = content.decode('utf-8', "ignore")
        return text

    def selector(self):
        if self.text is not None:
            try:
                resp = selector(res=self)
            except Exception:
                resp = None
            return resp

class Request:
    def __init__(self, url: Union[int, str], method: str = "GET", callback: str = "parse",
                 data: Union[dict, None] = None, params: Union[dict, None] = None, json: Union[dict, None] = None,
                 headers: Union[dict, None] = None, proxies: str = None, timeout: Union[int, float] = 3,
                 max_times: int = 3, cookies: Union[dict, None] = None, verify: bool = False,
                 is_async: bool = True,  allow_redirects=True, count=0, meta=None):
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
        self.count = count
        self.meta = meta

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
                if key in ["url", "method", "callback", "data", "json", "params", "callback", "count", "meta"]:
                    dic[key] = self.__dict__[key]
        return dic

    @property
    def domain_name(self):
        return re.search("(http|https)://(www.)?(\w+(\.)?)+", self.url).group()


class Item:
    def __init__(self, table_name=None, method="insql", request=None, **kwargs):
        self._kwargs = kwargs
        self.table_name = table_name
        self.method = method
        self.request = request
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def to_dict(self,):
        dic = {}
        for key in self.__dict__.keys():
            if self.__dict__[key]:
                if key not in ["table_name", "method", "request", "_kwargs"]:
                    dic[key] = self.__dict__[key]
        return dic

