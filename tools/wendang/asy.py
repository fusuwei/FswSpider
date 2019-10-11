import aiohttp, asyncio

aiohttp.request()
async def main(pool):  # 启动
    sem = asyncio.Semaphore(pool)
    async with aiohttp.ClientSession() as session:  # 给所有的请求，创建同一个session
        tasks = []
        [tasks.append(control_sem(sem, 'https://api.github.com/events?a={}'.format(i), session)) for i in
         range(10)]  # 十次请求
        await asyncio.wait(tasks)


async def control_sem(sem, url, session):  # 限制信号量
    async with sem:
        await fetch(url, session)


async def fetch(url, session):  # 开启异步请求
    async with session.get(url) as resp:
        json = await resp.json()
        print(json)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(pool=2))