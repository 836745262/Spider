from selenium import webdriver
import requests
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import os

url = 'https://wenku.baidu.com/view/fda543a8ce2f0066f4332212.html?from=search'
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14D27 Safari/602.1"')
# chromedriver = "/usr/local/chromedriver"
# os.environ["webdriver.chrome.driver"] = chromedriver
# browser = webdriver.Chrome(chrome_options=chrome_options,executable_path=chromedriver)
browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)


def search(url):
    try:
        browser.get(url)
        # click_butt = wait.until(EC.element_to_be_clickable(
        #     (By.CSS_SELECTOR,'#html-reader-go-more > div.continue-to-read > div.banner-more-btn')))
        #click_butt.click()
        #click_butt = wait.until(EC.element_to_be_clickable(
        #            (By.CSS_SELECTOR, '.pagerwg-loadSucc .pagerwg-arrow-lower')))

        # click_butt.click()

    except NoSuchElementException:
        print('requests failed')


def get_details(html):
    doc = pq(html)
    items = doc('#flow-ppt-wrap > div > div').items()
    i = 1
    for item in items:
        img_link = item.find('div.ppt-image-wrap > img').attr('src')
        save_img(img_link,i)
        i += 1
        print(img_link)


def save_img(img_link,i):
    try:
        response = requests.get(img_link)
        if response.status_code == 200:
            img = response.content
            with open('/Users/brianlee/desktop/img_%i.png'%i,'wb') as f:
                f.write(img)
    except Exception:
        print('failed')


def main():
    html = search(url)
    get_details(html)


if __name__ == '__main__':
    main()