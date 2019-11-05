from pyppeteer import launch
import asyncio

async def main():
    browser = await launch({
        'headless': False,
        # 'devtools': True,  # 打开 chromium 的 devtools
        'args': [
            '--disable-extensions',  # 禁用拓展。
            "-hide-scrollbars",  # 隐藏屏幕快照中的滚动条
            "--disable-bundled-ppapi-flash",  # 禁用Flash
            "--mute-audio",  # 静音
            "--no-sandbox",  # 禁用沙盒
            "--disable-setuid-sandbox",  # 禁用GDP
            "--disable-infobars"
        ],
        # 'dumpio': True,
        "userDataDir": r"D:\userDataDir",
    })  # 新建一个Browser对象
    page = await browser.newPage()  # 新建一个选项卡，page对象
    await page.setExtraHTTPHeaders({"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"})
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
    await page.goto('https://www.zhipin.com/job_detail/?query=&city=101200100&industry=&position=')
    await page.waitFor(1000)
    a = await page.xpath("//button[text()='搜索']")
    await page.waitFor(1000)
    await a[0].click()
    page.mouse
    await page.waitFor(1000)
    import time
    time.sleep(5)
    cookies = await page.cookies()
    cookie = {}
    for cook in cookies:
        cookie[cook["name"]] = cook["value"]
    await page.waitFor(3000)
    await page.close()
    await browser.close()  # 关闭模拟器
    return cookie


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


loop = asyncio.get_event_loop()  # 异步操作
future = loop.run_until_complete(main())
print(future)


from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
# def selenium_get_cookies(url, headless=True, executable_path=None, proxy=None):
#     if proxy:
#         proxy = proxy.replace("http://", '').replace("https://", '')
#     chrome_options = Options()
#     if headless:
#         chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument(
#         'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.3170.100 Safari/537.36"')
#     if proxy:
#         chrome_options.add_argument('--proxy-server=http://{}'.format(proxy))
#     if executable_path:
#         path = executable_path
#     else:
#         path = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
#     browser1 = webdriver.Chrome(path, chrome_options=chrome_options)
#     browser1.maximize_window()
#     browser1.get(url)
#     time.sleep(1)
#     a = browser1.find_element_by_xpath("//button[@class='btn btn-search']")
#     a.click()
#     time.sleep(1000)
#
#     cookieslist = browser1.get_cookies()
#     cookies = {}
#     for cook in cookieslist:
#         cookies[cook["name"]] = cook["value"]
#     browser1.close()
#     browser1.quit()
#     return cookies
# selenium_get_cookies("https://www.zhipin.com", headless=False)