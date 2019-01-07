import time, random
import requests
from urllib import parse
import hashlib
import json
import js2py


js1 = '''
    function signtest(e, t) {
        var n = e("./jquery-1.7");
        e("./utils");
        e("./md5");
        var r = function(e) {
            var t = n.md5(navigator.appVersion)
              , r = "" + (new Date).getTime()
              , i = r + parseInt(10 * Math.random(), 10);
            return {
                ts: r,
                bv: t,
                salt: i,
                sign: n.md5("fanyideskweb" + e + i + "p09@Bn{h02_BIEe]$P^nG")
            }
        }
'''


def getsalt():
    '''
    salt的形成："" + (new Date).getTime() + parseInt(10 * Math.random(), 10)
    '''
    salt = str(int(time.time() * 1000)) + str(random.randint(0, 10))

    return salt


def getts():
    # "" + (new Date).getTime()
    ts = int(time.time() * 1000)
    return ts


def getMD5(v):
    md5 = hashlib.md5()

    md5.update(v.encode('utf-8'))
    sign = md5.hexdigest()

    return sign


def getsign(key, salt):
    '''
    sign的形成:n.md5("fanyideskweb" + e + i + "p09@Bn{h02_BIEe]$P^nG")
    '''
    sign = "fanyideskweb" + key + str(salt) + "p09@Bn{h02_BIEe]$P^nG"
    sign = getMD5(sign)
    return sign


def getbv():
    bv = '5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
    bv = getMD5(bv)
    return bv


def youdao(key):
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

    salt = getsalt()
    sign = getsign(key, salt)
    ts = getts()
    bv = getbv()

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
    print(data)
    # 对data进行编码，因为data需要bytes类型数据
    data = parse.urlencode(data).encode()

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
        'Referer': 'http://fanyi.youdao.com/',
        'Host': 'fanyi.youdao.com',
        # 'Content-Length': bytes(len(data)),
        'Origin': 'http://fanyi.youdao.com',
        'Cookie': 'OUTFOX_SEARCH_USER_ID=-620380420@10.169.0.83; OUTFOX_SEARCH_USER_ID_NCOO=1725730399.7034585; JSESSIONID=aaaNXUPOf5N1O9R1xhJFw; ___rl__test__cookies=1545707147909',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    response = requests.post(url, data=data, headers=headers)
    translate = json.loads(response.text)['translateResult'][0][0]['tgt']
    print(translate)
    # print(len(data))

if __name__ == '__main__':
    # sign = js2py.eval_js(js1)
    # sign()
    while True:
        word = input('请输入需要翻译的内容:')
        youdao(word)
        if word == 'exit':
            break