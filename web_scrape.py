#!/usr/bin/env python

import re
import sys
import time
import random
import requests
from bs4 import BeautifulSoup as soup
from multiprocessing import Process, Queue, current_process, freeze_support

print('Which website shall we crawl?\n')


QUEUE_PROCESS = Queue()
QUEUE_COMPLETED = Queue()
MASTER_LIST = set([])

# domains = ['http://www.euromuenzen.com']
# domains = ['http://www.hamsterdance.org']
domains = ['http://www.sudokrew.com']


def scrape_func(input, output):
    for each_url in iter(input.get, 'STOP'):
        this_domain = each_url

        # Prepare for variety of events by separating URL in useful sections
        reg_split = re.match(r'(http.*\/\/)(\w+\.)?(\w+)(\.\w{3})', this_domain)
        
        http_tag = reg_split[1]
        pre_tag = reg_split[2]
        site_name = reg_split[3]
        domain_tag = reg_split[4]
        just_domain = '{}{}{}{}'.format(http_tag, pre_tag, site_name, domain_tag)
    
        full_page = requests.get(this_domain)
        if(full_page.status_code != 200): # If URL is not valid, disregard
            return
        else: 
            MASTER_LIST.add(this_domain)

        html = soup(full_page.text, 'html.parser')

        for anchor in html.find_all('a', href=True):
            a_link = anchor['href'] # Find all [a href] tags

            if(re.match(r'/', a_link)): # If link starts with '/' append it to primary domain
                a_link = just_domain + a_link

            if(re.match(r'http', a_link) and a_link not in MASTER_LIST):
                QUEUE_PROCESS.put(a_link)
                MASTER_LIST.add(a_link)
                QUEUE_COMPLETED.put(a_link)
                


def start_multi(arg):
    count = 0
    WORKER_NUMBERS = 8
    try:
        for i in range(WORKER_NUMBERS): # For number of Workers set, start individual scrape invocation
            p = Process(target=scrape_func, args=(QUEUE_PROCESS, QUEUE_COMPLETED))
            p.start()

        for each_domain in domains: # Put each URL in process queue
            QUEUE_PROCESS.put(each_domain)

        for each_completed in iter(QUEUE_COMPLETED.get, 'STOP'): # For each in complete queue, insert 'STOP'
            if count >= len(domains) - 1:
                for i in range(WORKER_NUMBERS):
                    QUEUE_PROCESS.put('STOP')
                return
            else:
                count = count + 1
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)


# Main Function 
def main(param):
    start_multi(param)

        
if __name__ == '__main__':
    main(domains)
