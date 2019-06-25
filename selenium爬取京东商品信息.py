from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
import pymongo
from config import *

client = pymongo.MongoClient(host=MONGO_URL,port=27017)
db = client[MONGO_DB]
collection = db[MONGO_TABLE]


url = 'https://www.jd.com/'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)

wait = WebDriverWait(browser,10)


def search():
    print('正在搜索网页...')
    try:
        browser.get(url)
        input_ = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,'#key'))
        )
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,'#search > div > div.form > button'))
        )
        input_.send_keys('美食')
        submit.click()
        total_page = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > em:nth-child(1) > b'))
        )
        return total_page.text
    except TimeoutException:
        search()


def next_page(page_number):
    print('正在翻页...')
    try:
        input_ = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > input'))
        )
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > a'))
        )
        input_.clear()
        input_.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR,'#J_bottomPage > span.p-num > a.curr'),str(page_number))
        )
        get_product()
    except TimeoutException:
        next_page(page_number)


def get_product():
    print('正在获取商品信息...')
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_goodsList')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#J_goodsList ul li.gl-item').items()
    for item in items:
        products = {
            'img':item.find('.p-img a img').attr('src'),
            'price':item.find('.p-price strong i').text(),
            'name':item.find('.p-name.p-name-type-2 a em').text().split('\n')[0],
            'sale':item.find('.p-commit strong a').text(),
            'shop':item.find('.p-shop span a').text()
        }
        # print(products)
        save_to_mongo(products)


def save_to_mongo(result):
    try:
        if collection.insert_one(result):
            print('存储成功')
    except Exception:
        print('存储失败')


def main():
    total = int(search())
    for page_n in range(1,total+1):
        next_page(page_n)
    browser.close()


if __name__ == '__main__':
    try:
        main()
    except Exception as result:
        print(result)
