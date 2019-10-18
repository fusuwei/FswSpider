from tools.user_agents import get_ua
from tools.proxy import get_ip, ip_process
from tools.toolslib import get_cookies


class DefaultMiddleware:
    def process_request(self, request, spider):
        if spider.auto_headers:
            request.headers["User-Agent"] = get_ua()
        if spider.auto_proxy:
            proxies = get_ip()
            request.proxies = ip_process(proxies, spider.is_async)
        if spider.auto_cookies:
            if spider.is_invalid:
                if request.proxies:
                    proxies = request.proxies.replace("http://", "").replace("https://", "")
                    cookies = get_cookies(request.domain_name, proxy=proxies)
                else:
                    cookies = get_cookies(request.domain_name)
                request.cookies = cookies