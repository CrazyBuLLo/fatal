import requests
import re
from bs4 import BeautifulSoup
import time
from multiprocessing import Pool
import re



phone_api = 'https://wuhan.anjuke.com/v3/ajax/broker/phone/?broker_id={}&token={}&prop_id={}'


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
}

# 需要保持会话
session = requests.Session()


# 解析索引页
def parse_index(i):
    url = 'https://wuhan.anjuke.com/sale/p{}/'.format(i)
    response = session.get(url, headers=headers)
    content = response.text
    detail_urls = re.findall('<a data-from.*href="(.*?)"', content)
    print(len(detail_urls))
    for detail_url in detail_urls:
        print(detail_url)
        time.sleep(1)
        get_telephone(detail_url)


# 获取电话的接口
def get_telephone(url):

    response = session.get(url, headers=headers)
    content = response.text
    tele_list = re.search(r".*PhoneNum[\s\S]*broker_id:'(\d+)'[\s\S]*token:(.*)[\s\S]*prop_id:(.*),", content)


    broker_id = tele_list.group(1)
    token = tele_list.group(2).replace("'", '').replace(',', '').strip()
    prop_id = tele_list.group(3).replace("'", '').strip()

    phone_uri = phone_api.format(broker_id, token, prop_id)
    phone_resp = session.get(phone_uri, headers=headers)
    phone = phone_resp.json()['val']
    print(phone)

def main():
    parse_index(1)


if __name__ == '__main__':

    # 创建进程池
    pool = Pool(5)
    # 异步非阻塞
    pool.apply_async(main)
    # 关闭进程
    pool.close()
    # 阻塞进程
    pool.join()