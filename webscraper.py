#!/usr/bin/env python

import time
import random
import requests
from urllib import request
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue, current_process, freeze_support

print('Which website shall we crawl?\n')

QUEUE_PROCESS = Queue()
QUEUE_COMPLETED = Queue()

def scrape_func(input, output):
    for domain in iter(input.get, 'STOP'):
        result = requests.get(domain)
        QUEUE_COMPLETED.put('for style')


def main():
    # List of domains
    domains = ['http://www.youtube.com', 'http://www.google.com', 'http://www.google.com', 'http://www.google.com', 'http://www.soranews24.com']

    WORKER_NUMBERS = 4


    for i in range(WORKER_NUMBERS):
        Process(target=scrape_func, args=(QUEUE_PROCESS, QUEUE_COMPLETED)).start()

    for each in domains:
        print('printing each domain in the list: ', each)
        QUEUE_PROCESS.put(each)

    count = 0

    for message in iter(QUEUE_COMPLETED.get, 'STOP'):
        print('what is count then length: ', count, len(domains))
        if count >= len(domains) - 1:
            for i in range(WORKER_NUMBERS):
                QUEUE_PROCESS.put('STOP')
            return
        else:
            count = count + 1

if __name__ == '__main__':
    main()
