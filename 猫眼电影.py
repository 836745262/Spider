import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool


def get_one_page(url):
    try:

        response = requests.get(url)
        if response.status_code == 200:
           return response
        return None
    except RequestException:
        return None


def parse_html(html):

    pattern = re.compile('<dd>.*?board-index-(\d+)">.*?</i>.*?<a.*?title="(.*?)".*?<p.*?star">'+
                         '(.*?)</p>.*?releasetime">(.*?)</p>.*?score.*?integer">(.*?)</i>'+
                  '.*?fraction">(.*?)</i>.*?</dd>',re.S)
    result = re.findall(pattern,html)
    for item in result:
        yield {
            'index':item[0],
            'name':item[1],
            'star':item[2].strip()[3:],
            'releasetime':item[3][5:],
            'score':item[4]+item[5]
        }


def save_text(item):
    with open('result.text','a',encoding='utf8') as f:
        f.write(json.dumps(item,ensure_ascii=False)+'\n')
        f.close()


def main(offset):
    url = 'https://maoyan.com/board/4?offset='+str(offset)
    response = get_one_page(url)
    print(response.text)
    result = parse_html(response.text)
    print('-'*50)
    for item in result:
        print(item)
        save_text(item)


if __name__ == '__main__':

#    for i in range(10):
#        main(i*10)
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])
