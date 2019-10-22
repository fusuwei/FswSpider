st = '''
Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,ja;q=0.8
Connection: keep-alive
Content-Length: 75
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: JSESSIONID=ABAAABAAAIAACBI50AEE079018936C1F1F851BB4843E551; WEBTJ-ID=20191022212415-16df3a3b52f20-0a060e2db327e7-b363e65-1049088-16df3a3b531112; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1571750656; _ga=GA1.2.648911852.1571750656; _gat=1; _gid=GA1.2.1810073550.1571750656; user_trace_token=20191022212415-3ea62c12-f4cf-11e9-9f93-525400f775ce; LGSID=20191022212415-3ea62e81-f4cf-11e9-9f93-525400f775ce; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DlAyoqGv225tn5XylOG3o5USj2hwq8f-NJ4lVm7VJpSK%26ck%3D8082.1.93.206.152.209.146.145%26shh%3Dwww.baidu.com%26wd%3D%26eqid%3Deed4fca4000e2fcc000000035daf02fc; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGUID=20191022212415-3ea63012-f4cf-11e9-9f93-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_search; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216df3a3d247311-05a3c648be4c2e-b363e65-1049088-16df3a3d248700%22%2C%22%24device_id%22%3A%2216df3a3d247311-05a3c648be4c2e-b363e65-1049088-16df3a3d248700%22%7D; sajssdk_2015_cross_new_user=1; SEARCH_ID=0be5380cb81a4a6aa5d87cffec84b20b; X_HTTP_TOKEN=8898454414a5ab5953905717514ec9c6744262d2cc; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1571750936; LGRID=20191022212856-e5aa0467-f4cf-11e9-9f93-525400f775ce
Host: www.lagou.com
Origin: https://www.lagou.com
Referer: https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36
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