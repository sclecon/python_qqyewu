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
        if url.find('qqyewu') > 0:
            char = 'gbk'
        html = html.decode(char)
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all('a', href=re.compile(r"/%s(\d{5})" % time.strftime('%Y%m%d', time.localtime())))
        for link in links:
            if link['href'] is None or link.get_text() is None or len(link.get_text()) == 0:
                continue
            data['url'].append("%s%s" % (url, link['href']))
            data['title'].append(link['title'])
            # print "href:%s    title:%s" % (link['href'],link.get_text())
        # print ''
        # print ''
        return data

    def DetailData(self, html, url):
        if html is None or url is None:
            return None
        if url.find('qqyewu') > 0:
            try:
                html = html.decode('gbk')
            except:
                html = html.decode('gbk')
            soup = BeautifulSoup(html, "html.parser")
            if url.find('article') > 0:
                return self.qqyewu_article_data(soup)
            elif url.find('soft') > 0:
                return self.qqyewu_soft_data(soup)
        
        return None

    def qqyewu_article_data(self, soup):
        data = {}
        data['title'] = soup.find('div', class_="newstit").find('h1').get_text().replace(u'\xa0', u' ')
        data['body'] = soup.find('div', class_="des").get_text().replace(u'\xa0', u' ')
        data['url_type'] = 'article'
        data['catyname'] = soup.find('div', class_="breadcrumb").find('a', href=re.compile(r"index.html")).get_text().replace(u'\xa0', u' ')
        # print data['catyname']
        return data

    def qqyewu_soft_data(self, soup):
        data = {}
        data['title'] = soup.find('div', class_="tit").find('h1').get_text().replace(u'\xa0', u' ')
        data['body'] = soup.find('div', class_="des").get_text().replace(u'\xa0', u' ')
        data['os'] = soup.find('li', class_="gw").find("span").get_text().replace(u'\xa0', u' ')
        download = soup.find('div', class_="DownloadSfotCon").find_all('li')
        downloader = download[0].find('a')
        data['downloader'] = downloader['href']
        data['url_type'] = 'soft'
        data['catyname'] = soup.find('div', class_="breadcrumb").find('a', href=re.compile(r"index.html")).get_text().replace(u'\xa0', u' ')
        # print data['catyname']
        return data