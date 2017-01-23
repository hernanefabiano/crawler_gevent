import gevent.monkey; gevent.monkey.patch_thread()
from bs4 import BeautifulSoup
import urllib
import urllib.request
import itertools
import random
import sys

import gevent.monkey; gevent.monkey.patch_all(thread=False)


class Crawler(object):


    def __init__(self):
        self.soup = None                                        
        self.current_page   = "http://probasketballtalk.com/"   
        self.links          = set()                             
        self.visited_links  = set()

        self.counter = 0 # Simple counter for debug purpose

    def crawl_page(self):

        print ('{}: {}'.format(self.counter, self.current_page))
        res = urllib.request.urlopen(self.current_page)
        html_code = res.read()
        self.visited_links.add(self.current_page)

        # Fetch every links
        self.soup = BeautifulSoup(html_code)

        page_links = []
        try:
            for link in [h.get('href') for h in self.soup.find_all('a')]:
                if link.startswith('http'):
                    page_links.append(link)
                elif link.startswith('/'):
                    parts = urllib.parse(self.current_page)
                    page_links.append(parts.scheme + '://' + parts.netloc + link)
                else:
                    page_links.append(self.current_page+link)
                
        except Exception as ex:
            # Magnificent exception handling
            print (ex)

        # Update links
        self.links = self.links.union(set(page_links))

        # Choose a random url from non-visited set
        self.current_page = random.sample(self.links.difference(self.visited_links), 1)[0]
        self.counter += 1

    def run(self):

        crawling_greenlets = []
        for i in range(3):
            crawling_greenlets.append(gevent.spawn(self.crawl_page))

            gevent.joinall(crawling_greenlets)

        for link in self.links:
            print (link)

if __name__ == '__main__':
    C = Crawler()
    C.run()
