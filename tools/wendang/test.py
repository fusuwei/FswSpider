import asyncio  # pyppeteer采用异步方式，需要导入
from pyppeteer import launch
from parsel import Selector
import time


async def main():
    browser = await launch({
        'headless': False,
        'devtools': True,  # 打开 chromium 的 devtools
        'args': [
            '--disable-extensions',  # 禁用拓展。
            "-hide-scrollbars",  # 隐藏屏幕快照中的滚动条
            "--disable-bundled-ppapi-flash",  # 禁用Flash
            "--mute-audio",  # 静音
            "--no-sandbox",  # 禁用沙盒
            "--disable-setuid-sandbox",  # 禁用GDP
            "--window-size=1366, 768"
        ],
        'dumpio': True,
    })  # 新建一个Browser对象
    page = await browser.newPage()  # 新建一个选项卡，page对象
    await page.setViewport({'width': 1366, 'height': 768})
    await page.evaluate("""
        () =>{
            Object.defineProperties(navigator,{
                webdriver:{
                get: () => false
                }
            })
        }
    """)  # 伪装
    await page.setRequestInterception(True)
    page.on('request', intercept_request)
    page.on('response', intercept_response)
    await page.goto('https://huaban.com/favorite/beauty/?k05bk3sz&max=2700259955&limit=20&wfl=2')
    time.sleep(12)
    content = await page.content() # 访问指定页面

    print(content)
    await browser.close()  # 关闭模拟器


async def intercept_request(req):
    """请求过滤"""
    if req.resourceType in ['image', 'media', 'eventsource', 'websocket']:
        await req.abort()
    else:
        await req.continue_()

async def intercept_response(res):
    resourceType = res.request.resourceType
    if resourceType in ['xhr', 'fetch']:
        resp = await res.text()
        print(resp)

asyncio.get_event_loop().run_until_complete(main())  # 异步操作