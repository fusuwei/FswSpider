import aiohttp
import requests
from tools import log
from tools.proxy import get_ip, ip_process
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


async def requesting(session, obj, Response, allow_code=None, is_async=True):
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
                            headers=headers, callback=obj.callback, proxies=obj.proxies, method=method)
        else:
            logger.error("第%d次请求！状态码为%s" % (abs(obj.max_times-3), status_code))
            return obj


async def request(spider, obj, channel, tag):
    """
            请求函数，
            :param message: list 爬虫信息
            :param channel:
            :param tag:
            :param properties:
            :return:
            """
    res = None
    while obj.max_times:
        obj.max_times -= 1
        callback = getattr(spider, obj.callback)
        spider.is_async = obj.is_async
        if hasattr(obj, "err"):
            err = getattr(obj, "err")
        if spider.auto_cookies and not spider.cookies:
            obj.auto_cookies(spider.auto_proxy)
            spider.cookies = obj.cookies
        if spider.auto_headers:
            obj.auto_headers()
        if spider.auto_proxy:
            obj.auto_proxy()
        logger.debug("开始请求url为：%s" % obj.url)
        obj = spider.remessage(obj)
        if obj.proxies:
            obj.proxies = ip_process(obj.proxies, obj.is_async)
        if not obj.domain_name:
            ret = callback(obj)
            return ret
        else:
            if spider._pre_domain_name != obj.domain_name and obj.domain_name is not None:
                if spider.session:
                    await close_session(session=spider.session)
                spider.session = await create_session(obj.is_async, obj.verify, obj.cookies)
            spider._pre_domain_name = obj.domain_name
            res = await requesting(spider.session, obj, spider.Response, allow_code=spider.allow_code)
            if isinstance(res, spider.Request):
                continue
            else:
                ret = callback(res)
                return ret
    spider.produce(res)
    channel.basic_ack(delivery_tag=tag)