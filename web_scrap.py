from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from selenium import webdriver
import requests
import time  # New import

def scraping(url):
    browser = webdriver.PhantomJS()
    browser.get(url)
    time.sleep(5)  # 5 seconds
    html = browser.page_source
    return BeautifulSoup(html, 'lxml')

# Get Html
page = scraping('https://leetcode.com/TommyTim0515/')
print(page.as_html())
# Extract price as str
# price = page.find("span", class_="text-success").getText()

# print(price)  # Outputs $3.74