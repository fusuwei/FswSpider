import asyncio
import aiohttp
import requests
from tools.built_in.log import log
import setting
import random
logger = log(__name__)

'''
 url=None, method="GET", data=None, params=None, headers=None, proxies=None, timeout=10,
                  json=None, cookies=None, allow_redirects=False, verify_ssl=False, limit=100, callback="parse",
                  max_times=3, auto_proxy=False, allow_code=None
'''
async def request(message, auto_proxy=False, allow_code=None):
    url = message.get("url", None)
    callback = message.get("callback", "parse")
    max_times = message.get("max_times", 3)
    method = message.get("method", "GET")
    data = message.get("data", None)
    params = message.get("params", None)
    headers = message.get("headers", None)
    proxies = message.get("proxies", None)
    timeout = message.get("timeout", 10)
    json = message.get("json", None)
    cookies = message.get("cookies", None)
    allow_redirects = message.get("allow_redirects", False)
    verify_ssl = message.get("verify_ssl", False)
    if auto_proxy:
        proxies = random.choice(setting.proxies)
    if url and "http" in url:
        conn = aiohttp.TCPConnector(verify_ssl=verify_ssl,)
        async with aiohttp.ClientSession(connector=conn, cookies=cookies) as session:
            max_times += 1
            for i in range(1, max_times):
                if proxies and "https" in proxies:
                    proxies = proxies.replace("https", "http")
                try:
                    if method.upper() == "GET":
                        async with session.get(url=url, params=params, headers=headers, proxy=proxies, timeout=timeout,
                                               allow_redirects=allow_redirects) as res:
                            content = await res.read()
                    elif method.upper() == 'POST':
                        async with session.post(url, data=data, headers=headers, proxy=proxies, timeout=timeout,
                                                allow_redirects=allow_redirects, json=json) as res:
                            content = await res.read()
                    else:
                        raise ValueError("method只支持post, get!")

                except Exception as e:
                    logger.error("请求失败，为返回Response")
                    if i == max_times:
                        content = None
                        error = e
                        return Response(url, content, error=error)
                    if auto_proxy:
                        proxies = random.choice(setting.proxies)
                        logger.debug("更换ip为：%s" % proxies)
                        continue
                else:
                    status_code = res.status
                    if status_code == 200 and content is not None:
                        charset = res.charset
                        cookies = res.cookies
                        headers = res.headers
                        text = _parse_content(charset, content)
                        return Response(url=url, content=content, status_code=status_code, text=text, cookies=cookies,
                                        headers=headers, callback=callback, proxies=proxies, )
                    elif allow_code and status_code in allow_code:
                        charset = res.charset
                        cookies = res.cookies
                        headers = res.headers
                        text = _parse_content(charset, content)
                        return Response(url=url, content=content, status_code=status_code, text=text, cookies=cookies,
                                        headers=headers, callback=callback, proxies=proxies, )
                    else:
                        proxies = random.choice(setting.proxies)
                        logger.debug("更换ip为：%s" % proxies)
                        logger.error("第%d次请求！状态码为%s" % (i, status_code))
    else:
        return message

def quest():
    return requests


def _parse_content(charset, content):
    if charset:
        try:
            text = content.decode(charset)
        except UnicodeDecodeError:
            try:
                text = content.decode('GBK')
            except UnicodeDecodeError:
                try:
                    text = content.decode('gb2312')
                except UnicodeDecodeError:
                    text = content.decode('utf-8', "ignore")
    else:
        try:
            text = content.decode('GBK')
        except UnicodeDecodeError:
            try:
                text = content.decode('GBK')
            except UnicodeDecodeError:
                try:
                    text = content.decode('gb2312')
                except UnicodeDecodeError:
                    text = content.decode('utf-8', "ignore")
    return text


class Response:
    def __init__(self, url, content=None, status_code=None, text=None, charset=None, cookies=None, method=None,
                 headers=None, callback="parse", proxies=None, error=None):
        self.url = url
        self.content = content
        self.status_code = status_code
        self.text = text
        self.charset = charset
        self.cookies = cookies
        self.method = method
        self.headers = headers
        self.callback = callback
        self.proxies = proxies
        self.error = error


if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    url = "https://www.baidu.com/"
    req = Myrequest()
    coroutine = req.request(url, headers=headers)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(coroutine)
    print()
