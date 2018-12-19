#!/usr/bin/env python

results = []

def dedupe_results():
    fd = open('scrape_results.txt', 'r')
    with fd as reader:
        for line in reader:
            if(len(line) > 1):
                results.append(line.rstrip())



dedupe_results()
results = list(set(results))
print(results)