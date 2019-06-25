from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
import re
import pymongo
from config import *

client = pymongo.MongoClient(host=MONGO_URL,port=27017)
db = client[MONGO_DB]
collection = db[MONGO_TABLE]

url = 'https://www.51job.com/?from=baidupz'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)

wait = WebDriverWait(browser,10)

def search():
    print('正在搜索网页...')
    try:
        browser.get(url)
        input_ = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,'#kwdselectid'))
        )
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,'body > div.content > div > div.fltr.radius_5 > div > button'))
        )
        input_.send_keys('证券')
        submit.click()
        total_page_text = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,'#resultList > div.dw_page > div > div > div > span:nth-child(2)'))
        )
        total_page = ''.join(re.findall('\d',total_page_text))
        return total_page
    except TimeoutException:
        search()

def next_page(page_number):
    print('正在翻页...')
    try:
        input_ = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,'#jump_page'))
        )
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,'#resultList > div.dw_page > div > div > div > span.og_but'))
        )
        input_.clear()
        input_.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR,'#resultList > div.dw_page > div > div > div > ul > li.on'),str(page_number))
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