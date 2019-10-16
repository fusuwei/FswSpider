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
import random
import time


async def worker(name, queue):
    while True:
        # Get a "work item" out of the queue.
        sleep_for = await queue.get()

        # Sleep for the "sleep_for" seconds.
        await asyncio.sleep(sleep_for)

        # Notify the queue that the "work item" has been processed.
        queue.task_done()

        print(f'{name} has slept for {sleep_for:.2f} seconds')


async def main():
    # Create a queue that we will use to store our "workload".

    # Create three worker tasks to process the queue concurrently.
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)

    # Wait until the queue is fully processed.
    started_at = time.monotonic()
    await queue.join()
    total_slept_for = time.monotonic() - started_at

    # Cancel our worker tasks.
    for task in tasks:
        task.cancel()
    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*tasks, return_exceptions=True)

    print('====')
    print(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
    print(f'total expected sleep time: {total_sleep_time:.2f} seconds')


queue = asyncio.Queue()
loop = asyncio.get_event_loop()
# Generate random timings and put them into the queue.
total_sleep_time = 0
for _ in range(20):
    sleep_for = random.uniform(0.05, 1.0)
    total_sleep_time += sleep_for
    loop.call_soon_threadsafe(queue.put_nowait, sleep_for)

asyncio.run(main())