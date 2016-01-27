#!/usr/bin/env python2.7
# -*- encoding: utf8 -*-
# Multi searcher by Nas @proclnas <proclnas@gmail.com>
#
# The MultiSearcher is an open source scan which uses some engines
# to find web sites with the use of keywords and phrases.
#
# Current engines:
# [ask, bing, rambler.ru]
#
# Made to be simple and fast, so this is not free of bugs. Submit if you find one.

import requests
import re
import os
import argparse
from sys import exit
from threading import Thread, Event
from Queue import Queue
from bs4 import BeautifulSoup


class MultiSearcher:
    def __init__(self, dork_file, output, threads):
        self.dork_file = dork_file
        self.output = output
        self.links = []
        self.ptr_limits = {
            'bing': 411,
            'ask': 20,
            'rambler': 20
        }
        self.exclude_itens = 'msn|microsoft|php-brasil|facebook|4shared|bing|imasters|phpbrasil|php.net|yahoo| \
                              scrwordtbrasil|under-linux|google|msdn|ask|bing|rambler|youtube'

        self.engines = {
            'bing': {
                'progress_string': '[Bing] Quering page {}/{} with dork {}\n',
                'search_string': 'http://www.bing.com/search?q={}&count=50&first={}',
                'page_range': xrange(1, self.ptr_limits['bing'], 10)
            },
            'ask': {
                'progress_string': '[Ask] Quering page {}/{} with dork {}\n',
                'search_string': 'http://www.ask.com/web?q={}&page={}',
                'page_range': xrange(1, self.ptr_limits['ask'])
            },
            'rambler': {
                'progress_string': '[Rambler.ru] Quering page {}/{} with dork {}\n',
                'search_string': 'http://nova.rambler.ru/search?query={}&page={}',
                'page_range': xrange(1, self.ptr_limits['rambler'])
            }
        }

        self.threads = threads
        self.q = Queue()
        self.t_stop = Event()
        self.counter = 0
        self.list_size = len(open(self.dork_file).readlines())

    def get_links(self, word, engine):
        self.links = []
        current_engine = self.engines[engine]

        for ptr in current_engine['page_range']:
            print current_engine['progress_string'].format(ptr, self.ptr_limits[engine], word)

            content = requests.get(current_engine['search_string'].format(word, str(ptr)))

            if content.ok:
                try:
                    soup = BeautifulSoup(content.text)

                    for link in soup.find_all('a'):
                        link = link.get('href')

                        if 'http' in link and not re.search(self.exclude_itens, link):

                            if link not in self.links:
                                self.links.append(link)
                                with open(self.output, 'a+') as fd:
                                    fd.write(link + '\n')
                except Exception:
                    pass

    def search(self, q):
        while not self.t_stop.is_set():
            self.t_stop.wait(1)

            try:
                word = q.get()
                self.get_links(word, 'bing')  # Bing
                self.get_links(word, 'ask')  # Ask
                self.get_links(word, 'rambler')  # Rambler

            except Exception:
                pass
            finally:
                self.counter += 1
                q.task_done()

    def main(self):
        for _ in xrange(self.threads):
            t = Thread(target=self.search, args=(self.q,))
            t.setDaemon(True)
            t.start()

        for word in open(self.dork_file):
            self.q.put(word.strip())

        try:
            while not self.t_stop.is_set():
                self.t_stop.wait(1)
                if self.counter == self.list_size:
                    self.t_stop.set()

        except KeyboardInterrupt:
            print '~ Sending signal to kill threads...'
            self.t_stop.set()
            exit(0)

        self.q.join()
        print 'Finished!'

if __name__ == "__main__":
    banner = '''
      __  __       _ _   _  _____                     _
     |  \/  |     | | | (_)/ ____|                   | |
     | \  / |_   _| | |_ _| (___   ___  __ _ _ __ ___| |__   ___ _ __
     | |\/| | | | | | __| |\___ \ / _ \/ _` | '__/ __| '_ \ / _ \ '__|
     | |  | | |_| | | |_| |____) |  __/ (_| | | | (__| | | |  __/ |
     |_|  |_|\__,_|_|\__|_|_____/ \___|\__,_|_|  \___|_| |_|\___|_|
     By @proclnas
    '''

    parser = argparse.ArgumentParser(description='Procz Multi Searcher')

    parser.add_argument(
        '-f', '--file',
        action='store',
        dest='dork_file',
        help='List with dorks to scan (One per line)',
        required=True
    )
    parser.add_argument(
        '-o', '--output',
        action='store',
        dest='output',
        help='Output to save valid results',
        default='output.txt'
    )
    parser.add_argument(
        '-t', '--threads',
        action='store',
        default=1,
        dest='threads',
        help='Concurrent workers (By word)',
        type=int
    )
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()

    if args.dork_file:
        if not os.path.isfile(args.dork_file):
            exit('File {} not found'.format(args.dork_file))

        print banner
        multi_searcher = MultiSearcher(args.dork_file, args.output, args.threads)
        multi_searcher.main()
