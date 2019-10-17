import aiohttp
import asyncio


async def a():
    client_session = aiohttp.ClientSession()
    resp = await client_session.get("https://www.baidu.com", )
    async with resp:
        assert resp.status == 200
        return client_session


async def c(client_session):
    resp = await client_session.get("https://www.baidu.com", )
    async with resp:
        print(resp.status)
        await client_session.close()

loop = asyncio.get_event_loop()
future = loop.run_until_complete(a())
print(future)
loop.run_until_complete(c(future))
loop = asyncio.get_running_loop()