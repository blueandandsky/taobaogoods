from urllib.parse import quote

from pyquery import PyQuery
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
KEYWORD = 'iPad'
MAX_PAGE = 10

# TODO 不能通过验证

'''抓取索引页'''


def index_page(page):
    print('正在获取第', page, '页')
    url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
    browser.get(url)

    try:
        if page > 1:
            input = wait.until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, '#mainsrp-pager div,form > input')))
            submit = wait.until(expected_conditions.element_to_be_clickable(
                (By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)
            submit.click()
            wait.until(expected_conditions.text_to_be_present_in_element(
                (By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
            wait.until(expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, '.m-itemlist .items .item')))
            get_products()
    except TimeoutException:
        index_page(page)


'''提取商品数据'''


def get_products():
    html = browser.page_source
    doc = PyQuery(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('title').text(),
            'shop': item.find('shop').text(),
            'location': item.find('.location').text()
        }
        print(product)


'''遍历每一页'''


def main():
    for i in range(1, MAX_PAGE + 1):
        index_page(i)


if __name__ == '__main__':
    main()
    browser.close()
