st = '''
Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
Content-Length: 75
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: JSESSIONID=ABAAABAAAFCAAEGB56FAC2810A6F67A84B89859382CAFAC; WEBTJ-ID=20191022144320-16df234a7f413e-08e680a3524a9f-3d375b01-2073600-16df234a7f6ad8; _gid=GA1.2.390333950.1571726600; _ga=GA1.2.2047833536.1571726600; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1571726601; user_trace_token=20191022144405-5789355d-f497-11e9-9f79-525400f775ce; LGUID=20191022144405-5789380f-f497-11e9-9f79-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216df2361e483a3-0a6505e9181b4-3d375b01-2073600-16df2361e4a6e2%22%2C%22%24device_id%22%3A%2216df2361e483a3-0a6505e9181b4-3d375b01-2073600-16df2361e4a6e2%22%7D; X_MIDDLE_TOKEN=8a6fb71aa8cc6d87bdf464fca78dc395; TG-TRACK-CODE=index_search; SEARCH_ID=65e68d8f239b449fa2913b6e4c8110ac; X_HTTP_TOKEN=63bac72f5aba70fb41282717513edafad355ec3170; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1571728169; LGRID=20191022151016-ffc473ff-f49a-11e9-a604-5254005c3644
Host: www.lagou.com
Origin: https://www.lagou.com
Pragma: no-cache
Referer: https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36
X-Anit-Forge-Code: 0
X-Anit-Forge-Token: None
X-Requested-With: XMLHttpRequest

'''
for i in st.split('\n'):
    if i:
        if i.startswith(':'):
            i = i[1:]
            i = i.replace(':', "':'", 1)
            i = ':' + i
        else:
            i = i.replace(':', "':'", 1).replace(' ','',1)
        i = "'" + i + "'" + ","

        print(i)