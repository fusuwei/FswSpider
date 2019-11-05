# import requests
#
#
# headers = {
# "Cookie":"lastCity=101200100; _uab_collina=156679703305887683362765; _bl_uid=7Rk2F1w2lqtjC2n6R7aglkygw5va; __c=1571985264; __g=-; __l=l=%2Fwww.zhipin.com%2Fweb%2Fcommon%2Fsecurity-check.html%3Fseed%3DsGWCUWnCegBV8Kz0JYsazgJ8QxINQapHVrUGQQt5Qg4%253D%26name%3Dbdb61485%26ts%3D1571985305131%26callbackUrl%3D%252Fjob_detail%252F%253Fquery%253D%2526city%253D101070100%2526industry%253D%2526position%253D%26srcReferer%3Dhttps%253A%252F%252Fwww.zhipin.com%252F&r=https%3A%2F%2Fwww.zhipin.com%2F&friend_source=0&friend_source=0; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1571985281; __zp_stoken__=8c4aoy%2B7W0qNKAmcUKgZq%2FrRrLzfuSA29R9TiwUZSWui9TlN%2FYxpIWvMp6H633OYaVTSLO4rII87knNVjJnYyfIN2Q%3D%3D; __a=53203235.1571985264..1571985264.4.1.4.4; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1571985285",
# 'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
# }
# session = requests.session()
# ret = session.get("https://www.zhipin.com/c101200100/?page=2&ka=page-2", headers=headers)
#
# print()
# a = {'__a': '7109279.1571904386.1571904386.1571906663.3.2.2.3', 'lastCity': '101200100', 'Hm_lvt_194df3105ad7148dcf2b98a91b5e727a': '1571904330,1571904386,1571906663', '__c': '1571906663', '__g': '-', 'Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a': '1571906663', '__l': 'l=%2Fwww.zhipin.com%2F&r=&friend_source=0&friend_source=0'}
# print('; '.join(k+ '=' + v for k, v in a.items())+"; ")


# import aiohttp
# import asyncio
# import requests
#
# async def req():
#     print("--------------------")
#     conn = aiohttp.TCPConnector(verify_ssl=True, limit=100)
#     async with aiohttp.ClientSession(connector=conn,)as session:
#
#         res = await session.get("https://www.baidu.com/")
#
#         await res.text()
#         print("==================")
#         print(res.status)
#
# tasks = [
#     req() for i in range(10)
# ]
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(tasks))
import time
import execjs
import requests
from urllib import parse
import re
import os
# os.environ["PATH"] = os.environ["PATH"]+";;D:\Program Files\\nodejs\\"
# os.environ["NODE"] = "D:\Program Files\\nodejs\\"
os.environ["EXECJS_RUNTIME"] = "Node"
headers = {
    'cookie':'__zp_stoken__=eeddGGL%2B26w0qCAhKv5OnqNF%2BxDXsTRHAcSJeQY6e8LZQ%2BQPsba0lcq3CFCIbaLQLSVd1kKy6DpedWLEJKM60oWSfw%3D%3D',
    # 'pragma':'no-cache',
    # 'sec-fetch-mode':'navigate',
    # 'sec-fetch-site':'same-origin',
    # 'sec-fetch-user':'?1',
    'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
}
with open(r"F:\js\a.js\aa.js", "r", encoding="utf8")as f:
    row = f.read()
fun = execjs.compile(row)
# ret = fun.call("f")
# execjs.get()
ret = fun.call("fun", '3Nc3krc/lfTgzIZdLfy7I3z9jNFtGBMEM5i8WuSxXQQ=', 1572961184908)
print(ret)
# seed = None
# ts = None
# for i in range(1, 10):
#     url = "https://www.zhipin.com/c101200100/?query=web%E5%89%8D%E7%AB%AF&page={}&ka=page-{}".format(i, i)
#     if i == 1:
#         res1 = requests.get(url, headers=headers, allow_redirects=False)
#         seed = re.search("seed=(.*?)&", res1.headers["location"]).group(1)
#         ts = re.search("ts=(.*?)&", res1.headers["location"]).group(1)
#         seed = parse.unquote_plus(seed)
#     ret = parse.quote_plus(fun.call("aaa", seed, ts))
#     print(ret)
#     headers = {
#         'cookie':'__zp_stoken__='+ret,
#         'pragma':'no-cache',
#         'sec-fetch-mode':'navigate',
#         'sec-fetch-site':'same-origin',
#         'sec-fetch-user':'?1',
#         'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
#     }
#     res2 = requests.get(url, headers=headers)
#     cook = res2.cookies.get_dict()
#     seed = cook["__zp_sseed__"]
#     ts = cook["__zp_sts__"]
#     print(res2)

