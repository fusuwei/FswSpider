from tools.user_agents import get_ua
from tools.proxy import ip_process, get_ip
from tools.toolslib import get_cookies
import tools
import re
logger = tools.log(__name__)


def middleware(message, auto_headers=False, auto_cookies=False, auto_proxy=False):
    url = message["url"]
    if url:
        domain_name = re.search("(http|https)://(www.)?(\w+(\.)?)+", url).group()
        message["domain_name"] = domain_name
    if "is_async" in message:
        is_async = message["is_async"]
    else:
        is_async, message["is_async"] = True, True
    proxies = message.get("proxies", '')
    if proxies:
        ip_process(proxies, is_async)

    if auto_headers:
        headers = message.get("headers", "")
        if headers:
            ua = get_ua()
            if "User-Agent" in headers:
                headers["User-Agent"] = ua
            elif "user-agent" in headers:
                headers["user-agent"] = ua
            else:
                headers["User-Agent"] = ua
            logger.debug("自动设置user-agent为：%s" % ua)
            message["headers"] = headers
        else:
            ua = get_ua()
            message["headers"] = {"User-Agent": ua}
            logger.debug("自动设置user-agent为：%s" % ua)

    if auto_cookies:
        if proxies:
            proxies = proxies.replace("http://").replace("https://")
            cookies = get_cookies(message["url"], proxy=proxies)
        elif auto_proxy:
            proxies = get_ip()
            cookies = ''
            if proxies:
                proxies = proxies.replace("http://").replace("https://")
                cookies = get_cookies(message["url"], proxy=proxies)
        else:
            cookies = message.get("cookies", tools.get_cookies(url=message["url"]))
        logger.debug("自动设置获取cookies为：%s" % cookies)
        headers = message.get("headers", "")
        if headers:
            if "cookies" in headers:
                headers["cookies"] = cookies
            elif "Cookies" in headers:
                headers["Cookies"] = cookies
            else:
                headers["Cookies"] = cookies
            message["headers"] = headers
            message["proxies"] = proxies
        else:
            ua = get_ua()
            message["headers"] = {"User-Agent": ua, "Cookies": cookies}
    return message
