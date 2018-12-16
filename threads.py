#!/usr/bin/env python

from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup as soup

all_urls = [
        'http://www.google.com',
        # 'http://www.cnn.com'
]

def scrape(url):
        res = requests.get(url)
#     print(res.status_code, res.url)
        html = soup(res.text, 'html.parser')
        for anchor in html.find_all('a', href=True):
            a_link = anchor['href']
            print('a_link: ', a_link)

p = Pool(10)
p.map(scrape, all_urls)
p.terminate()
p.join()