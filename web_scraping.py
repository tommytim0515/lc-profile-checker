import time
import regex as re
from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display

CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
URL_PREFIX = 'https://leetcode.com/'
ACCPET_KEYWORD = 'Accepted'
ACCEPT_TOKENS = ('minute', 'minutes', 'hour', 'hours')
PAGE_LOAD_TIME = 5  # seconds
EXTENDED_PAGE_LOAD_TIME = 10  # seconds
RETRY_NUM = 5


def scraping(url: str, page_load_timeout: int) -> BeautifulSoup:
    display = Display(visible=0, size=(800, 800))
    display.start()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--disable-plugins-discovery')
    driver = webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH, options=chrome_options)
    # driver.set_page_load_timeout(10)
    driver.delete_all_cookies()
    driver.get(url)

    time.sleep(page_load_timeout)
    html = driver.page_source
    display.stop()

    return BeautifulSoup(html, 'lxml')


def check_today_submission(user_name: str, page_load_timeout: int) -> bool:
    page = scraping(URL_PREFIX + user_name, page_load_timeout)
    profile_root = page.find('div', id='profile-root')
    profile_content = profile_root.find(
        'div', {'class': re.compile('^profile-content_')})
    ant_cards = profile_content.find_all(
        'div', {'class': re.compile('^ant-card ')})
    submission_items = ant_cards[-1].find_all(
        'li', {'class': re.compile('^ant-list-item')})
    for item in submission_items:
        item_text = item.text
        if ACCPET_KEYWORD not in item_text:
            continue
        for token in ACCEPT_TOKENS:
            if token in item_text:
                print(item_text)
                return True
    return False

def check_today_submission_with_retry(user_name: str, retry_count: int) -> bool:
    if check_today_submission(user_name, PAGE_LOAD_TIME):
        return True
    if retry_count <= 0:
        return False
    while retry_count > 0:
        if check_today_submission(user_name, EXTENDED_PAGE_LOAD_TIME):
            return True
        retry_count -= 1
    return False


if __name__ == '__main__':
    print(check_today_submission_with_retry('TommyTim0515', RETRY_NUM))
