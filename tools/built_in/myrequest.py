import aiohttp
import requests
from tools import log
from tools.proxy import get_ip
logger = log(__name__)


async def create_session(is_async=True, verify_ssl=True, cookies=None):
    if is_async:
        conn = aiohttp.TCPConnector(verify_ssl=verify_ssl, limit=100)
        session = aiohttp.ClientSession(connector=conn, cookies=cookies)
    else:
        session = requests.Session()
        session.cookies = requests.utils.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)
        session.verify = verify_ssl
    return session


async def close(session):
    await session.close()


def close_session(session, is_async=True):
    if is_async:
        import asyncio
        loop=asyncio.get_event_loop()
        loop.run_until_complete(close(session))
        loop.close()
    else:
        session.close()


async def request(url, session, message=None, auto_proxy=False, allow_code=None, is_async=True):
    callback = message.get("callback", "parse")
    max_times = message.get("max_times", 3)
    method = message.get("method", "GET")
    data = message.get("data", None)
    params = message.get("params", None)
    headers = message.get("headers", None)
    proxies = message.get("proxies", None)
    timeout = message.get("timeout", 10)
    json = message.get("json", None)
    allow_redirects = message.get("allow_redirects", False)
    if "http" in url and session:
        for i in range(1, max_times+1):
            content = None
            if auto_proxy and not proxies:
                proxies = get_ip()
                logger.debug("更换ip为：%s" % proxies)
            try:

                if method.upper() == "GET":
                    if is_async:
                        async with session.get(url=url, params=params, headers=headers, proxy=proxies, timeout=timeout,
                                               allow_redirects=allow_redirects) as res:
                            content = await res.read()
                            status_code = res.status
                            charset = res.charset
                    else:
                        res = session.get(url, params=params, headers=headers, proxy=proxies, timeout=timeout,
                                          allow_redirects=allow_redirects)
                        content = res.content
                        status_code = res.status_code
                        charset = res.encoding

                elif method.upper() == 'POST':
                    if is_async:
                        async with session.post(url, data=data, headers=headers, proxy=proxies, timeout=timeout,
                                                allow_redirects=allow_redirects, json=json) as res:
                            content = await res.read()
                            status_code = res.status
                            charset = res.charset
                    else:
                        res = session.post(url, data=data, headers=headers, proxy=proxies, timeout=timeout,
                                           json=json, allow_redirects=allow_redirects)
                        content = res.content
                        status_code = res.status_code
                        charset = res.encoding
                else:
                    raise ValueError("method只支持post, get!")
            except Exception as e:
                logger.error("请求失败，为返回Response")
                if i == max_times:
                    return Response(url, content, error=e)
            else:
                if status_code == 200 and content is not None:
                    cookies = res.cookies
                    headers = res.headers
                    text = _parse_content(charset, content)
                    return Response(url=url, content=content, status_code=status_code, text=text, cookies=cookies,
                                    headers=headers, callback=callback, proxies=proxies, )
                elif allow_code and status_code in allow_code:
                    cookies = res.cookies
                    headers = res.headers
                    text = _parse_content(charset, content)
                    return Response(url=url, content=content, status_code=status_code, text=text, cookies=cookies,
                                    headers=headers, callback=callback, proxies=proxies, )
                else:
                    logger.error("第%d次请求！状态码为%s" % (i, status_code))
    else:
        return message


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
    import asyncio
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    url = "http://www.baidu.com/"
    loop = asyncio.get_event_loop()
    session = loop.run_until_complete(create_session(verify_ssl=True))
    coroutine = request(url, session, message={})

    coroutine1 = close_session(session)
    a = loop.run_until_complete(coroutine)
    loop.run_until_complete(coroutine1)
    print(a.content)