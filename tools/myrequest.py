import asyncio
import aiohttp
import requests
from tools.log import logger


class Myrequest:
    def __init__(self):
        pass

    async def request(self, url =None, method="GET", data=None, params=None, headers=None, proxies=None, timeout=10,
            json=None, cookies=None,allow_redirects=False, verify_ssl=False, limit=100):

        self.conn = aiohttp.TCPConnector(verify_ssl=verify_ssl, limit=limit)

        async with aiohttp.ClientSession(connector=self.conn, cookies=cookies) as self.session:
            try:
                if method.upper() == "GET":
                    async with self.session.get(url=url, params=params, headers=headers, proxy=proxies, timeout=timeout,
                                           allow_redirects=allow_redirects) as res:
                        content = await res.read()
                elif method.upper() == 'POST':
                    async with self.session.post(url, data=data, headers=headers, proxy=proxies, timeout=timeout,
                                            allow_redirects=allow_redirects, json=json) as res:
                        content = await res.read()
                else:
                    raise ValueError("method只支持post, get!")
            except Exception as e:
                content = None
                logger.error("请求未返回res")
                return Response(url, content)
            else:
                status_code = res.status
                charset = res.charset
                cookies = res.cookies
                headers = res.headers
                text = self._parse_content(charset, content)
                return Response(url=url, content=content, status_code=status_code, text=text, cookies=cookies, headers=headers)

    def quest(self):
        return requests

    def _parse_content(self, charset, content):
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
    def __init__(self, url, content=None, status_code=None, text=None, charset=None, cookies=None, method=None, headers=None):
        self.url = url
        self.content = content
        self.status_code = status_code
        self.text = text
        self.charset = charset
        self.cookies = cookies
        self.method = method
        self.headers = headers


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
