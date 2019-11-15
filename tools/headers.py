st = '''
Accept: */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,ja;q=0.8
AccessToken: 4FPNXVU3G2WJ6TFW3O2VXHF52JUE4IYVEKZNZMEB7VT46IPD2LRQ110ac98
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded;charset=UTF-8
Cookie: api_uid=CiGG0F2tfqu7lQBEI5vKAg==; JSESSIONID=0498C843242F008520460161D54D24E4
Host: apiv3.yangkeduo.com
Origin: http://yangkeduo.com
Referer: http://yangkeduo.com/search_catgoods.html?opt_id=9503&opt1_id=999998&opt2_id=999999&opt_g=1&opt_type=3&opt_name=%E5%8D%AB%E8%A1%A3&_x_link_id=c4e848bf-7e23-4d8d-be15-0c1a9dd45038&refer_page_name=search&refer_page_id=10031_1573731526920_E15DghjaHW&refer_page_sn=10031
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36
VerifyAuthToken: e4SplzhDIRDrsX4OSwpUmg
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