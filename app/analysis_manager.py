#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

class analysis_manager(object):
	def analysis_nowurls(self, html, url):
		data = []
		if html is None or url is None:
			return data
		char = 'utf-8'
		if url == 'http://www.qqyewu.com':
			char = 'gb2312'
		html = html.decode(char)
		data.append('http://www.666.com');
		print html.find_all('a')
		
		return data