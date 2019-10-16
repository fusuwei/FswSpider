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
        if verify_ssl:
            verify_ssl = False
        else:
            verify_ssl = True
        session = requests.Session()
        session.cookies = requests.utils.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)
        session.verify = verify_ssl
    return session


async def close_session(session, is_async=True):
    if is_async:
        await session.close()
    else:
        session.close()


async def request(session, obj, Response, auto_proxy=False, allow_code=None, is_async=True):
    method = obj.method
    try:
        if method.upper() == "GET":
            if is_async:
                async with session.get(url=obj.url, params=obj.params, headers=obj.headers, proxy=obj.proxies,
                                       timeout=obj.timeout, allow_redirects=obj.allow_redirects) as res:
                    content = await res.read()
                    status_code = res.status
                    charset = res.charset
            else:
                res = session.get(obj.url, params=obj.params, headers=obj.headers, proxies=obj.proxies,
                                  timeout=obj.timeout,
                                  allow_redirects=obj.allow_redirects)
                content = res.content
                status_code = res.status_code
                charset = res.encoding

        elif method.upper() == 'POST':
            if is_async:
                async with session.post(obj.url, data=obj.data, headers=obj.headers, proxy=obj.proxies,
                                        timeout=obj.timeout,
                                        allow_redirects=obj.allow_redirects, json=obj.json) as res:
                    content = await res.read()
                    status_code = res.status
                    charset = res.charset
            else:
                res = session.post(obj.url, data=obj.data, headers=obj.headers, proxies=obj.proxies,
                                   timeout=obj.timeout,
                                   json=obj.json, allow_redirects=obj.allow_redirects)
                content = res.content
                status_code = res.status_code
                charset = res.encoding
        else:
            raise ValueError("method只支持post, get!")

    except Exception as e:
        logger.error("请求失败，未返回Response")
        obj.err = e
        return obj
    else:
        if (status_code == 200 and content is not None) or status_code in allow_code:
            cookies = res.cookies
            headers = res.headers
            return Response(url=obj.url, content=content, status_code=status_code, charset=charset, cookies=cookies,
                            headers=headers, callback=obj.callback, proxies=obj.proxies, method=method, request=obj)
        else:
            logger.error("第%d次请求！状态码为%s" % (abs(obj.max_times-3), status_code))
            return obj
