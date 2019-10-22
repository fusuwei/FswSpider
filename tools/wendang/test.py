# import asyncio  # pyppeteer采用异步方式，需要导入
#
# from pyppeteer import launch
# from parsel import Selector
# import time
# "executablePath"
#
#
# async def main():
#     browser = await launch({
#         'headless': True,
#         # 'devtools': True,  # 打开 chromium 的 devtools
#         'args': [
#             '--disable-extensions',  # 禁用拓展。
#             "-hide-scrollbars",  # 隐藏屏幕快照中的滚动条
#             "--disable-bundled-ppapi-flash",  # 禁用Flash
#             "--mute-audio",  # 静音
#             "--no-sandbox",  # 禁用沙盒
#             "--disable-setuid-sandbox",  # 禁用GDP
#         ],
#         # 'dumpio': True,
#         "userDataDir": r"D:\userDataDir",
#     })  # 新建一个Browser对象
#     page = await browser.newPage()  # 新建一个选项卡，page对象
#     await page.setViewport({'width': 1366, 'height': 768})
#     cookies = await page.cookies("https://huaban.com/favorite/beauty/?k05bk3sz&max=2700259955&limit=20&wfl=2")
#     print(cookies)
#     # await page.evaluate("""
#     #     () =>{
#     #         Object.defineProperties(navigator,{
#     #             webdriver:{
#     #             get: () => false
#     #             }
#     #         })
#     #     }
#     # """)  # 伪装
#     # await page.setRequestInterception(True)
#     # page.on('request', intercept_request)
#     # page.on('response', intercept_response)
#     # await page.goto('https://huaban.com/favorite/beauty/?k05bk3sz&max=2700259955&limit=20&wfl=2')
#     # await page.waitFor(1000)
#     # cookies = await page.cookies()
#     # print(cookies)
#     await page.waitFor(3000)
#     await page.close()
#     await browser.close()  # 关闭模拟器
#     return cookies
#
#
# async def intercept_request(req):
#     """请求过滤"""
#     if req.resourceType in ['image', 'media', 'eventsource', 'websocket']:
#         await req.abort()
#     else:
#         await req.continue_()
#
#
# async def intercept_response(res):
#     resourceType = res.request.resourceType
#     if resourceType in ['xhr', 'fetch']:
#         resp = await res.text()
#         print(resp)
#
# loop = asyncio.get_event_loop()  # 异步操作
# future = loop.run_until_complete(main())
# print(future)

#
#
# # import aiohttp
# # import asyncio
# # async  def a():
# #     client_session = aiohttp.ClientSession()
# #     resp = await client_session.get("https://www.baidu.com", )
# #     async with resp:
# #         assert resp.status == 200
# #         return client_session
# #
# #
# # async def c(client_session):
# #     resp = await client_session.get("https://www.baidu.com", )
# #     async with resp:
# #         print(resp.status)
# #         await client_session.close()
# #
# # loop = asyncio.get_event_loop()
# # future = loop.run_until_complete(a())
# # print(future)
# # loop.run_until_complete(c(future))
#
# # import asyncio
# # import time
# #
# #
# # def ret(a):
# #     time.sleep(3)
# #     return a
# #
# #
# # async def get_text(index_url):
# #     try:
# #         print(index_url,",","1")
# #         loop = asyncio.get_event_loop()
# #         # 主要在这
# #         resp = await loop.run_in_executor(None, ret, index_url)
# #         print(index_url,",","2","-",resp)
# #     except Exception as err:
# #         # 出现异常重试
# #         print(err)
# #         return None
# #     return resp
# #
# # tasks = []
# # for i in range(0, 3):
# #     tasks.append(get_text(i))
# # # 获取EventLoop:
# # loop = asyncio.get_event_loop()
# # # 执行coroutine
# # loop.run_until_complete(asyncio.wait(tasks))
# # loop.close()
# from typing import (  # noqa
#     Any,
#     Coroutine,
#     Generator,
#     Generic,
#     Iterable,
#     List,
#     Mapping,
#     Optional,
#     Set,
#     Tuple,
#     Type,
#     TypeVar,
#     Union,
# )
#
# # def a(i: Union[str, int] = None) -> Union[str, int]:
# #     print(i)
# #     return i
# # b = object()
# # a(b)
# import asyncio
# import threading
# import time
#
# q = asyncio.Queue()
#
# async def ping():
#     while True:
#         await asyncio.sleep(10)
#         print("ping")
#
# async def rcv():
#     while True:
#         item = await q.get()
#         print("got item")
#
# async def run():
#     tasks = [asyncio.ensure_future(ping()), asyncio.ensure_future(rcv())]
#     await asyncio.wait(tasks, return_when="FIRST_EXCEPTION")
#
# loop = asyncio.get_event_loop()
#
# def run_loop():
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(run())
#
# threading.Thread(target=run_loop).start()
#
# while True:
#     time.sleep(2)
#     loop.call_soon_threadsafe(q.put_nowait, "item")
#     print("item added")

import asyncio
import threading



# def threaded(loop):
#     import time
#     while True:
#         time.sleep(2)
#         loop.call_soon_threadsafe(queue.put_nowait, time.time())
#         loop.call_soon_threadsafe(lambda: print(queue.qsize()))
#
#
# async def asyncd():
#     while True:
#         time = await queue.get()
#         print(time)
#
# loop = asyncio.get_event_loop()
# queue = asyncio.Queue(loop=loop)
# threading.Thread(target=loop.run_until_complete, args=(asyncd(), )).start()
# # threading.Thread(target=threaded, args=(loop, )).start()
# threaded(loop)


# import asyncio
#
# async def a ():
#     print('-------------')
#     await asyncio.sleep(10)
# loop = asyncio.get_event_loop()
# tasks = []
# for i in range(10):
#
# loop.run_forever()
# loop.run_until_complete(asyncio.wait(tasks))

# url = '123'
# req = type("Request", (), {"url": url})
# print()
# import asyncio
#
#
# async def da():
#     return 1
#
# async def a():
#     print("----------------")
#     d = await da()
#     print(d)
#     await asyncio.sleep(10)
#     print('==================')
#
# loop = asyncio.get_event_loop()
# tasks = []
# for i in range(10):
#     tasks.append(a())
#
# loop.run_until_complete(asyncio.wait(tasks))

# import requests
# import time
# session = requests.session()
# headers = {
#     'Host': 'www.lagou.com',
#     'Origin': 'https://www.lagou.com',
#     'Referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
# }
# url = 'https://www.lagou.com'
# ret = session.get(url, headers=headers)
# c = requests.cookies.RequestsCookieJar()
# a = {'LGUID': '20191022215752-f075835b-f4d3-11e9-a604-5254005c3644', 'PRE_LAND': 'https%3A%2F%2Fwww.lagou.com%2F', 'PRE_SITE': '', 'LGSID': '20191022215752-f07581d1-f4d3-11e9-a604-5254005c3644', 'user_trace_token': '20191022215752-f07580c7-f4d3-11e9-a604-5254005c3644', '_gid': 'GA1.2.1826648091.1571752672', 'LGRID': '20191022215752-f0758304-f4d3-11e9-a604-5254005c3644', 'PRE_HOST': '', '_ga': 'GA1.2.189801769.1571752672', 'PRE_UTM': '', 'JSESSIONID': 'ABAAABAAADEAAFIBF0B65782D0482AD2F981ACB4F49E968', '_gat': '1', 'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1571752672', 'X_HTTP_TOKEN': '42daf4b72327b2812762571751bf5e71415983ed09', 'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1571752672', 'WEBTJ-ID': '10222019%2C215751-16df3c27a7f166-047b5b75f4f1c3-72222910-480000-16df3c27a80265'}
# for k,v in a.items():
#     c.set(k, v)
# session.cookies.update(c)
# url1 = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
# data = {
# 'first':'false',
# 'pn':'2',
# 'kd':'爬虫',
# 'sid':'2dd815cd8cfb401baf957f11e8022cbd',
# }
# time.sleep(1)
# ret1 = session.post(url1, data=data, headers=headers)
# print()
import aiohttp
headers = {
    'Host': 'www.lagou.com',
    'Origin': 'https://www.lagou.com',
    'Referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
}
coo = {'LGUID': '20191022215752-f075835b-f4d3-11e9-a604-5254005c3644', 'PRE_LAND': 'https%3A%2F%2Fwww.lagou.com%2F', 'PRE_SITE': '', 'LGSID': '20191022215752-f07581d1-f4d3-11e9-a604-5254005c3644', 'user_trace_token': '20191022215752-f07580c7-f4d3-11e9-a604-5254005c3644', '_gid': 'GA1.2.1826648091.1571752672', 'LGRID': '20191022215752-f0758304-f4d3-11e9-a604-5254005c3644', 'PRE_HOST': '', '_ga': 'GA1.2.189801769.1571752672', 'PRE_UTM': '', 'JSESSIONID': 'ABAAABAAADEAAFIBF0B65782D0482AD2F981ACB4F49E968', '_gat': '1', 'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1571752672', 'X_HTTP_TOKEN': '42daf4b72327b2812762571751bf5e71415983ed09', 'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1571752672', 'WEBTJ-ID': '10222019%2C215751-16df3c27a7f166-047b5b75f4f1c3-72222910-480000-16df3c27a80265'}
import time
async def a():
    conn = aiohttp.TCPConnector(verify_ssl=False, limit=100)
    async with aiohttp.ClientSession(connector=conn, headers=headers,) as session:
        async with session.get('https://www.lagou.com') as resp:
            # session.cookie_jar.update_cookies(coo)
            print(resp.status)
            time.sleep(1)
            data = {
'first':'false',
'pn':'2',
'kd':'爬虫',
'sid':'2dd815cd8cfb401baf957f11e8022cbd',
}
            rl1 = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
            async with session.post(rl1, data=data,  headers=headers) as resp1:
                con = await resp1.read()
                con = con.decode()
                print(resp.status)
import asyncio
asyncio.run(a())