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
MASTER_LIST = {}

def scrape_func(input, output):
    for each_input in iter(input.get, 'STOP'):
        print('youchui', each_input)
        full_page = requests.get(each_input)

        if(full_page.status_code != 200):
            return

        html = soup(full_page.text, 'html.parser')
        for anchor in html.find_all('a', href=True):
            a_link = anchor['href']
            print('a_link: ', a_link)
            # Eval if URL is proper format (not local, as of now) 
            if(bool(re.search('www.', a_link)) & True): 
 
                main_domain = re.search(r'(www\.\w+\.\w{3})', a_link)

                # print('haa', main_domain[1])
                if(main_domain is not None):
                    main_domain = main_domain[1]
                    if(not hasattr(MASTER_LIST, main_domain )):
                        MASTER_LIST[main_domain] = []
                    if(main_domain in MASTER_LIST and not a_link in MASTER_LIST[main_domain]):
                        MASTER_LIST[main_domain].append(a_link)
                        QUEUE_PROCESS.put(a_link)
            # print('nyo?', MASTER_LIST)
            QUEUE_COMPLETED.put(links)


def main():
    def execute(arg):
        count = 0
        WORKER_NUMBERS = 4

        try:
            arg_page = requests.get(arg[0])
            # For every worker, use PROCESS to start multiple iterations of functions executing and processing concurrently
            for i in range(WORKER_NUMBERS):
                p = Process(target=scrape_func, args=(QUEUE_PROCESS, QUEUE_COMPLETED))
                p.daemon = True
                p.start()


            # Put all search criteria in the queue to be processed
            for each_domain in domains:
                QUEUE_PROCESS.put(each_domain)


            for each in iter(QUEUE_COMPLETED.get, 'STOP'):
                if count >= len(domains) - 1:
                    for i in range(WORKER_NUMBERS):
                        QUEUE_PROCESS.put('STOP')
                    return
                else:
                    count = count + 1
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)
        

    domains = []
    # user_input = input('Enter URL to crawl: ')
    user_input = 'google.com'
    # URL is entered with www.*.com
    if(bool(re.match('http://', user_input)) is False and bool(re.match('www.', user_input)) is True):
        user_input = 'https://{}'.format(user_input)
        domains.append(user_input)
        execute(domains)

    # URL is entered as *.com, *.org, or *.net
    elif(bool(re.match('http://www.', user_input)) is False) and bool(re.match('.+\.(?:com|org|net)', user_input)) is True:
        user_input = 'https://www.{}'.format(user_input)
        domains.append(user_input)
        execute(domains)

    else:
        print('Not a valid URL!')

    # Currently hard-coded, this will eventually be the initial set of all websites to be scraped
    # domains = ['http://www.soranews24.com']
    # domains = ['http://www.google.com', 'http://www.bing.com']
    # domains = ['http://www.google.com']

    # Possibly customizable variables in following iterations
    
if __name__ == '__main__':
    main()
