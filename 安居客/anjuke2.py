import requests
import re
from bs4 import BeautifulSoup
import time
import random
from multiprocessing import Pool
import re
from lxml import etree
import MySQLdb
import MySQLdb.cursors



phone_api = 'https://wuhan.anjuke.com/v3/ajax/broker/phone/?broker_id={}&token={}&prop_id={}'

conn = MySQLdb.connect('localhost', 'root', '1234', 'anjuke', charset='utf8', use_unicode=True)
cursor = conn.cursor()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
}

user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
]

def get_proxy():
    return requests.get("http://127.0.0.1:8080/get/").content

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:8080/delete/?proxy={}".format(proxy))

# your spider code

def getHtml():
    # ....
    retry_count = 5
    proxy = get_proxy()
    while retry_count > 0:
        try:
            html = requests.get('https://www.example.com', proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    # 出错5次, 删除代理池中代理
    delete_proxy(proxy)
    return None


# 需要保持会话
session = requests.Session()


# 解析索引页
def parse_index(i):
    global headers
    headers['user-agent'] = random.choice(user_agent)
    url = 'https://wuhan.anjuke.com/sale/p{}/'.format(i)

    proxy = get_proxy().decode('utf-8')
    print('using proxy %s' % proxy)

    try:
        response = session.get(url, headers=headers, proxies={"http": "http://{}".format(proxy)})
        print(response.status_code)
    except Exception:
        print('再次请求第%d页' % i)
        return parse_index(i)

    content = response.text
    detail_urls = re.findall('<a data-from.*href="(.*?)"', content)
    print(len(detail_urls))
    for detail_url in detail_urls:
        # time.sleep(0.5)
        get_html(detail_url)


# 获取电话的接口
def get_html(url):
    global headers
    headers['user-agent'] = random.choice(user_agent)
    retry_count = 3
    proxy = get_proxy().decode('utf-8')
    print('using proxy %s' % proxy)
    while retry_count > 0:
        try:

            response = session.get(url, headers=headers, proxies={"http": "http://{}".format(proxy)})
            print(response.status_code)
            content = response.text
            return parse_detail(content, url)
        except Exception:
            retry_count -= 1

    print('get_html None')
    return None

def parse_detail(content, url):
    global headers
    headers['user-agent'] = random.choice(user_agent)

    tele_list = re.search(r".*PhoneNum[\s\S]*broker_id:'(\d+)'[\s\S]*token:(.*)[\s\S]*prop_id:(.*),", content)

    html = etree.HTML(content)
    long_title = html.xpath("//h3[@class = 'long-title']/text()")[0].strip()
    xiaoqu = html.xpath("//div[@class = 'houseInfo-content']/a[@_soj = 'propview']/text()")[0]

    locations = html.xpath("//div[@class = 'houseInfo-content']/p[@class = 'loc-text']//text()")
    locations = ''.join([location.replace('\n', '').replace('\t', '') for location in locations])

    house_info = html.xpath("//p[@class = 'houseInfo']/text()")[0].split('，')
    house_info = [a.strip() for a in house_info]
    huxing = house_info[0]
    square = float(house_info[1].replace('m²', ''))
    cost = float(house_info[2].replace('万', ''))

    broker_id = tele_list.group(1)
    token = tele_list.group(2).replace("'", '').replace(',', '').strip()
    prop_id = tele_list.group(3).replace("'", '').strip()

    phone_uri = phone_api.format(broker_id, token, prop_id)

    retry_count = 3
    proxy = get_proxy().decode('utf-8')
    print('using proxy %s' % proxy)
    while retry_count > 0:
        try:

            phone_resp = session.get(phone_uri, headers=headers, proxies={"http": "http://{}".format(proxy)})
            print(phone_resp.status_code)
            return parse_phone(phone_resp, prop_id, long_title, xiaoqu, locations, huxing, square, cost, url)
        except Exception:
            retry_count -= 1

    print('parse_detail None')
    return None

def parse_phone(phone_resp, prop_id, long_title, xiaoqu, locations, huxing, square, cost, url):

    phone = phone_resp.json()['val'].replace(' ', '')

    item = {
        'id': prop_id,
        'long_title': long_title,
        'xiaoqu': xiaoqu,
        'locations': locations,
        'huxing': huxing,
        'square': square,
        'cost': cost,
        'phone': phone,
        'url': url
    }

    print(item)
    return insert_to_mysql(prop_id, long_title, xiaoqu, locations, huxing, square, cost, phone, url)


def insert_to_mysql(prop_id, long_title, xiaoqu, locations, huxing, square, cost, phone, url):
    insert_sql = """
        insert into wuhan2(prop_id, long_title, xiaoqu, locations, huxing, square, cost, phone, url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) on DUPLICATE key UPDATE locations = VALUES(locations),
         cost = VALUES(cost), phone = VALUES(phone), square = VALUES(square)
    """
    cursor.execute(insert_sql, (prop_id, long_title, xiaoqu, locations, huxing, square, cost, phone, url))
    conn.commit()


def main():
    for i in range(1, 51):
        parse_index(i)
    print('finish')


if __name__ == '__main__':

    # # 创建进程池
    # pool = Pool(5)
    # # 异步非阻塞
    # pool.apply_async(main)
    # # 关闭进程
    # pool.close()
    # # 阻塞进程
    # pool.join()
    main()