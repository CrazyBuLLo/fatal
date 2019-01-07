import js2py
import execjs
import time, random
import requests
from urllib import parse
import hashlib
import json

def get_js():
    f = open("md5.js", 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr




def youdao(key):
    jsstr = get_js()
    ctx = execjs.compile(jsstr)
    t = '5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
    data = ctx.call('signtest', key, t)

    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

    salt = data['salt']
    sign = data['sign']
    ts = data['ts']
    bv = data['bv']

    data = {
        'i': key,
        'from':'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,
        'sign': sign,
        'ts': ts,
        'bv': bv,
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTIME',
        'typoResult': 'false'

    }
    # print(data)
    # 对data进行编码，因为data需要bytes类型数据
    data = parse.urlencode(data).encode()

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
        'Referer': 'http://fanyi.youdao.com/',
        'Host': 'fanyi.youdao.com',
        'Content-Length': bytes(len(data)),
        'Origin': 'http://fanyi.youdao.com',
        'Cookie': 'OUTFOX_SEARCH_USER_ID=-620380420@10.169.0.83; OUTFOX_SEARCH_USER_ID_NCOO=1725730399.7034585; JSESSIONID=aaaNXUPOf5N1O9R1xhJFw; ___rl__test__cookies=1545707147909',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    response = requests.post(url, data=data, headers=headers)
    print(response)
    translate = json.loads(response.text)['translateResult'][0][0]['tgt']
    print(translate)


if __name__ == '__main__':
    youdao(input('请输入要翻译的词:'))


