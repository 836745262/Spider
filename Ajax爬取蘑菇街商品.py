import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode
import json
from json.decoder import JSONDecodeError
import re
def get_page_index(page,number):
    data = {
    'callback': 'jQuery21109161072303767281_1555928765030',
    '_version': 8193,
    'ratio': '3:4',
    'cKey': 15,
    'page': 1,
    'sort': 'pop',
    'ad': 0,
    'fcid': 52026,
    'action': 'food',
    '_': int('15559287650'+str(number))
    }
    params = urlencode(data)
    url = 'https://list.mogujie.com/search'+'?'+params
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return  response.text
        return None
    except RequestException:
        print('请求失败！')
        return None


def parse_page_index(text):
    try:
        pattern = re.compile('/\*\*/j.*?030\((.*?)\);',re.S)
        data = re.findall(pattern,text)
        # print(data[0])
        json_data = json.loads(data[0])
        if json_data and "result" in json_data.keys():
            for item in json_data["result"]["wall"]['docs']:
                yield item.get("link")
    except JSONDecodeError:
        pass


def get_page_detail(url):
    response = requests.get(url)
    try:
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求失败！',url)


# def parse_page_detail(html):


def main():
    html = get_page_index(1,31)
    # print(html,type(html))
    for url in parse_page_index(html):
        print(url)
        # print(get_page_detail(url))

if __name__ == '__main__':
    main()