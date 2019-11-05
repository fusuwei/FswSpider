st = '''
cookie: lastCity=101200100; _uab_collina=156679703305887683362765; _bl_uid=7Rk2F1w2lqtjC2n6R7aglkygw5va; __c=1572501925; __g=-; __l=l=%2Fwww.zhipin.com%2Fweb%2Fcommon%2Fsecurity-check.html%3Fseed%3DV9ry26ijYVFE6IA9M6Ah%252BKy5%252F2rkr%252BLqYWNPA%252Bh7SZc%253D%26name%3Db25cd80d%26ts%3D1572501997872%26callbackUrl%3D%252Fc101200100%252F%253Fquery%253Dweb%2525E5%252589%25258D%2525E7%2525AB%2525AF%2526page%253D3%2526ka%253Dpage-3%26srcReferer%3Dhttps%253A%252F%252Fwww.zhipin.com%252Fc101200100%252F%253Fquery%253Dweb%2525E5%252589%25258D%2525E7%2525AB%2525AF%2526page%253D2%2526ka%253Dpage-2&r=https%3A%2F%2Fwww.zhipin.com%2Fc101200100%2F%3Fquery%3Dweb%25E5%2589%258D%25E7%25AB%25AF%26page%3D2%26ka%3Dpage-2&friend_source=0; __a=27153194.1572501925..1572501925.1.1.1.1; __zp_stoken__=eeddGGL%2B26w0qCAhKv5OnqNF%2BxDXsTRHAcSJeQY6e8LZQ%2BQPsba0lcq3CFCIbaLQLSVd1kKy6DpedWLEJKM60oWSfw%3D%3D
pragma: no-cache
referer: https://www.zhipin.com/web/common/security-check.html?seed=V9ry26ijYVFE6IA9M6Ah%2BKy5%2F2rkr%2BLqYWNPA%2Bh7SZc%3D&name=b25cd80d&ts=1572501997872&callbackUrl=%2Fc101200100%2F%3Fquery%3Dweb%25E5%2589%258D%25E7%25AB%25AF%26page%3D3%26ka%3Dpage-3&srcReferer=https%3A%2F%2Fwww.zhipin.com%2Fc101200100%2F%3Fquery%3Dweb%25E5%2589%258D%25E7%25AB%25AF%26page%3D2%26ka%3Dpage-2
sec-fetch-mode: navigate
sec-fetch-site: same-origin
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36
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