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

import requests

url = 'https://buff.163.com/api/market/goods?game=csgo&page_num=4&_=1571367862061'
# headers={
#     'Accept':'application/json, text/javascript, */*; q=0.01',
# 'Accept-Encoding':'gzip, deflate, br',
# 'Accept-Language':'zh-CN,zh;q=0.9',
# 'Cache-Control':'no-cache',
# 'Connection':'keep-alive',
# # 'Cookie':'__root_domain_v=.163.com; _qddaz=QD.pownlj.k9f274.jv0mxvqq; _ga=GA1.2.1070801632.1556437903; _ntes_nnid=1c1909fcfc0c01b702376c25a33b9281,1556437906497; _ntes_nuid=1c1909fcfc0c01b702376c25a33b9281; UM_distinctid=16cb36744d7659-040e14e5f81ae5-3c375f0d-1fa400-16cb36744d860c; hb_MA-BFF5-63705950A31C_source=www.baidu.com; mail_psc_fingerprint=5788af9d36f0e0ffa8dc04b73746b9b9; ne_analysis_trace_id=1571360001914; s_n_f_l_n3=b01b39f12bb9e2511571360001918; _antanalysis_s_id=1571360002280; vinfo_n_f_l_n3=b01b39f12bb9e251.1.2.1566377985347.1568871730232.1571360043505; csrf_token=80acb585100202efba7f45aa5a7406af2dce7e45; game=csgo; _gid=GA1.2.153986468.1571367585; NTES_YD_SESS=AyZj3wbpegIcdVwXUE8Fzy6YcGEl2vuWG0TDskfKttvzBlf2BpU6VjpM3ZkYUu1QSSjClidujAw1bWHdU61YQxj03KIXf5Q.cp1vVpoF_qk1Y.H8fKyCspp_hxQYjVlWQ3iJGjv4TFqFjRskIk8g1RCa.1u.73jzdJn_NqEV4VVeMg6ZQ._5oArszU6aEAHS0ICF_OW4wExCRTAgsCU.966sF1Q2WFkn_1_AA7gpt2daC; S_INFO=1571367737|0|3&80##|17061315803; P_INFO=17061315803|1571367737|1|netease_buff|00&99|zhj&1571059698&g37_client#hub&420100#10#0#0|&0|null|17061315803; session=1-huFmoGCnva8i2qi_4tqMTkXQvW_4mH2tqIgIikdNz2SB2043395372; Locale-Supported=zh-Hans',
# 'Host':'buff.163.com',
# 'Pragma':'no-cache',
# 'Referer':'https://buff.163.com/market/?game=csgo',
# 'Sec-Fetch-Mode':'cors',
# 'Sec-Fetch-Site':'same-origin',
# 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
# 'X-Requested-With':'XMLHttpRequest',
# "Cookie" :"session=1-DUfVKFfpwzZw6lk0gj6XYtgJ0jZTTNH8sipZA7Z0devQ2046769729; P_INFO=18866674052|1571380159|1|netease_buff|00&99|hongkong&1571316120&gp#hub&420100#10#0#0|&0|null|18866674052; NTES_YD_SESS=2s2kscDrzGdc_5bcxa7qzk8Kw1Vqe0pl.G_YgOJvmm9n.6Js.4TFkU4bajXl17SJp4Y4p.r81XtMPfjLSky1Y.Am2vRNiBflTJhNclhiIFkeis6BOJ_LjS4CS7rMUk6zrAZtPU9d_0Ipab63kP1XU28L8Eh8RAUnitaCpIfkdkkdnZk8zSF2z7fY7eZeHqvvBWZLwH98ILxG9IsmuoOaedG1g1xLGYdIMNA5_pAZ_P8aB; _gat_gtag_UA_109989484_1=1; _gid=GA1.2.1484635456.1571380081; game=csgo; _ga=GA1.2.1218642560.1571380081; S_INFO=1571380159|0|3&80##|18866674052; csrf_token=77e7f18d766ef12fbb31c4a208cfa593ee804d1e",
# }
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2', 'Cookie': 'session=1-0lxLAatk0ngIbvPJ0jn7vc6P1ckVDxtNB8Dwf_9U3_Tz2046654463; P_INFO=18866478984|1571382331|1|netease_buff|00&99|JO&1571381631&g91_client#hub&420100#10#0#0|&0|null|18866478984; NTES_YD_SESS=jmamZVyVc36PaBea2_CK7JPW861eQEeFZDtzTchCxxBSukdfbTgqEaPMG4seKFLO0zCg5s8JSMjM4L0KCT_6qPhwc5aIGaCKEZm1IvsZC6U7PNaGWWlGF_0mpdRnfLOKR8FSYfBltoVLsIiaK5naiOf31bN1i8fv6S9mqVuLlLLyAL9GWUL2RaomT8bSNm4vUvdpYHC3gxpyX0d5NAlqU6Dh2ZZq13djHxpb7W1R8bt4Q; _gat_gtag_UA_109989484_1=1; _gid=GA1.2.268443136.1571382249; game=csgo; _ga=GA1.2.923934886.1571382249; S_INFO=1571382331|0|3&80##|18866478984; csrf_token=f38f55a9ab8bbe5c48060d89fb2e7865ea80e046'}
ret = requests.get(url, headers=headers)
print()

# """
# <class 'dict'>: {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2', 'Cookie': 'session=1-0lxLAatk0ngIbvPJ0jn7vc6P1ckVDxtNB8Dwf_9U3_Tz2046654463; P_INFO=18866478984|1571382331|1|netease_buff|00&99|JO&1571381631&g91_client#hub&420100#10#0#0|&0|null|18866478984; NTES_YD_SESS=jmamZVyVc36PaBea2_CK7JPW861eQEeFZDtzTchCxxBSukdfbTgqEaPMG4seKFLO0zCg5s8JSMjM4L0KCT_6qPhwc5aIGaCKEZm1IvsZC6U7PNaGWWlGF_0mpdRnfLOKR8FSYfBltoVLsIiaK5naiOf31bN1i8fv6S9mqVuLlLLyAL9GWUL2RaomT8bSNm4vUvdpYHC3gxpyX0d5NAlqU6Dh2ZZq13djHxpb7W1R8bt4Q; _gat_gtag_UA_109989484_1=1; _gid=GA1.2.268443136.1571382249; game=csgo; _ga=GA1.2.923934886.1571382249; S_INFO=1571382331|0|3&80##|18866478984; csrf_token=f38f55a9ab8bbe5c48060d89fb2e7865ea80e046'}
# """