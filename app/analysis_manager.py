#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import time

class analysis_manager(object):
        
    def analysis_nowurls(self, html, url):
        data = {'url': [], 'title':[]}
        if html is None or url is None:
            return data
        char = 'utf-8'
        if url == 'http://www.qqyewu.com':
            char = 'gb2312'
        html = html.decode(char)
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all('a', href=re.compile(r"/%s(\d{5})" % time.strftime('%Y%m%d', time.localtime())))
        for link in links:
            if link['href'] is None or link.get_text() is None or len(link.get_text()) == 0:
                continue
            data['url'].append(link['href'])
            data['title'].append(link.get_text())
            print "href:%s    title:%s" % (link['href'],link.get_text())
        print ''
        print ''
        return data