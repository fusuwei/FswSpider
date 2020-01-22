import re
from urllib import parse
import execjs
import requests


class BossZhiPin:
    def process_request(self, response, spider):
        if response.status_code == 302:
            seed = re.search("seed=(.*?)&", response.headers["location"]).group(1)
            seed = parse.unquote_plus(seed)
            ts = re.search("ts=(.*?)&", response.headers["location"]).group(1)
            jsname = re.search("name=(.*?)&", response.headers["location"]).group(1)
            jsurl = "https://www.zhipin.com/web/common/security-js/%s.js" % jsname
            js = requests.get(jsurl, headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',})
            js1 = """
                var window={"outerWidth":1920, "innerWidth":0, "Firebug":undefined,"outerHeight":1040,"innerHeight":0,
                "dispatchEvent":function (a) {return true},
                "navigator":{"userAgent":{"toLowerCase":function () { return "mozilla/5.0 (windows nt 6.1; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/77.0.3865.120 safari/537.36"},
                        "webdriver":false},
                    "appVersion":"5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"},
                "screen":{
                    "availHeight":1040,"availTop":0,"height":1080
                },
                "callPhantom":undefined,
                "_phantom":undefined,
                "moveTo":true,
                "moveBy":function () {},
                "open":function () {},
            };
            var document = {
                "getElementById":function (glcanvas) {return null},
                "title":"dasdasda",
                "createElement":function (str) {return str}
            };
            window.open.toString= function () {
                return "function open() { [native code] }"
            };
            top = {"location":
                    {"href":"https://www.zhipin.com/c101190100-p100101/?page=2&ka=page-2"}
            };
            exec = eval;
            """
            js2 = re.sub("setInterval(.*?)0x1f4\);", "", js.text)
            js3 = """
            func = function (e, i) {
                s = (new ABC).z(e, parseInt(i) + 60 * (480 + (new Date).getTimezoneOffset()) * 1e3);
                console.info(s)
                return s
            }
            """
            js = js1+js2+js3
            fun = execjs.compile(js)
            ret = parse.quote_plus(fun.call("func", seed, ts))
            spider.headers["cookie"] = '__zp_stoken__='+ret
        return response, spider