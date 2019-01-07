import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
    'referer': 'https://guangzhou.anjuke.com/sale/p3/'
}

def parse_index():
    # for i in range(51):
    url = 'https://guangzhou.anjuke.com/sale/p1/'
    response = requests.get(url, headers=headers)
    print(response.text)

if __name__ == '__main__':
    parse_index()