import aiohttp
import requests
from requests.cookies import RequestsCookieJar
import setting
from tools import log
from tools.proxy import ip_process
from tools import Response, Request
from importlib import import_module
import time
try:
    from tools.middleware import DefaultMiddleware
except Exception:
    pass
logger = log(__name__)


def import_libs(spider_name):
    Spider_Middleware, Downloader_Middleware = None, None
    if hasattr(setting, "SPIDER_MIDDLEWARE"):
        spider_middleware_dict = getattr(setting, "SPIDER_MIDDLEWARE")
        spider_middleware = spider_middleware_dict.get(spider_name, "")
        if spider_middleware:
            spider_path, spider_pack = spider_middleware.rsplit(".", maxsplit=1)
            Spider_Middleware = import_module(spider_path)
            Spider_Middleware = getattr(Spider_Middleware, spider_pack)()

    if hasattr(setting, "DOWNLOADER_MIDDLEWARES"):
        dowmloader_middleware_dict = getattr(setting, "DOWNLOADER_MIDDLEWARES")
        dowmloader_middleware = dowmloader_middleware_dict.get(spider_name, "")
        if dowmloader_middleware:
            dowmloader_path, dowmloader_pack = dowmloader_middleware.rsplit(".", maxsplit=1)
            Downloader_Middleware = import_module(dowmloader_path)
            Downloader_Middleware = getattr(Downloader_Middleware, dowmloader_pack)()

    return Spider_Middleware, Downloader_Middleware


def middleware(func, ):
    def inner(spider, object, *args, **kwargs):
        try:
            dm = DefaultMiddleware()
            request, spider = dm.process_request(object, spider)
        except Exception:
            pass
        Spider_Middleware, Downloader_Middleware = import_libs(spider.spider_name)
        if isinstance(object, Request):
            if Spider_Middleware:
                request, spider = Spider_Middleware.process_request(object, spider)
        elif isinstance(object, Response):
            if Downloader_Middleware:
                response, spider = Downloader_Middleware.process_request(object, spider)
        return func(spider, object, *args, **kwargs)
    return inner

@middleware
def downloader(spider, object):
    return object


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

@middleware
async def requesting(spider, request, max_times=3):
    method = request.method
    session = spider.session
    is_async = spider.is_async
    Response = spider.Response
    allow_code = spider.allow_code
    if request.cookies:
        if is_async:
            session.cookie_jar.update_cookies(request.cookies)
        else:
            cook = RequestsCookieJar()
            for k, v in request.cookies.items():
                cook.set(k, v)
            session.cookies.update(cook)
    if spider.download_delay:
        time.sleep(spider.download_delay)
    if spider.timeout:
        timeout = spider.timeout
    else:
        timeout = request.timeout
    try:
        if method.upper() == "GET":
            if is_async:
                async with session.get(url=request.url, params=request.params, headers=request.headers,
                                       proxy=request.proxies,
                                       timeout=timeout, allow_redirects=request.allow_redirects) as res:
                    content = await res.read()
                    status_code = res.status
                    charset = res.charset
            else:
                res = session.get(request.url, params=request.params, headers=request.headers,
                                  proxies=request.proxies,
                                  timeout=timeout,
                                  allow_redirects=request.allow_redirects)
                content = res.content
                status_code = res.status_code
                charset = res.encoding

        elif method.upper() == 'POST':
            if is_async:
                async with session.post(request.url, data=request.data, headers=request.headers, proxy=request.proxies,
                                        timeout=timeout,
                                        allow_redirects=request.allow_redirects, json=request.json) as res:
                    content = await res.read()
                    status_code = res.status
                    charset = res.charset
            else:
                res = session.post(request.url, data=request.data, headers=request.headers, proxies=request.proxies,
                                   timeout=timeout,
                                   json=request.json, allow_redirects=request.allow_redirects, )
                content = res.content
                status_code = res.status_code
                charset = res.encoding
        else:
            raise ValueError("method只支持post, get!")

    except Exception as e:
        logger.error("请求失败，未返回Response")
        request.err = e
        spider.is_invalid = True
        return request
    else:
        if (status_code == 200 and content is not None) or status_code in allow_code:
            spider.is_invalid = False
            cookies = res.cookies
            headers = res.headers
            return Response(url=request.url, content=content, status_code=status_code, charset=charset, cookies=cookies,
                            headers=headers, callback=request.callback, proxies=request.proxies, method=method,
                            meta=request.meta)
        else:
            spider.is_invalid = True
            logger.error("第%d次请求！状态码为%s" % (abs(max_times-3), status_code))
            return request


async def request(spider, request,):
    """
            请求函数，
            :param message: list 爬虫信息
            :param channel:
            :param tag:
            :param properties:
            :return:
            """
    res = None
    if spider.max_times:
        max_times = spider.max_times
    else:
        max_times = request.max_times
    while max_times:
        max_times -= 1
        callback = getattr(spider, request.callback)
        spider.is_async = request.is_async
        logger.debug("开始请求url为：%s" % request.url)
        if request.proxies:
            request.proxies = ip_process(request.proxies, spider.is_async)
        if not request.domain_name:
            ret = callback(request)
            return ret
        else:
            if spider._pre_domain_name != request.domain_name and request.domain_name is not None:
                if spider.session:
                    await close_session(session=spider.session)
                spider.session = await create_session(spider.is_async, request.verify, spider.cookies)
            spider._pre_domain_name = request.domain_name
            print("开始请求：", request.url)
            res = await requesting(spider, request, max_times=max_times)
            if isinstance(res, spider.Request):
                continue
            else:
                res = downloader(spider, res)
                if isinstance(res, spider.Request):
                    continue
                ret = callback(res)
                if res == ret:
                    return request
                return ret
    res.count += 1
    return res


