#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests

class Request(object):
	
	def set_rooturl(self, url):
		if url is None:
			return None
		super(Request, self).__init__()
		self.url = url
		return True

	def set_charset(self, charset):
		if charset is None:
			return None
		super(Request, self).__init__()
		self.charset = charset
		return True

	def get_html_content(self, url=False):
		if self.url is None or self.charset is None:
			return None
		if url is False:
			url = self.url
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
		try:
			response = requests.get(url, headers=headers)
			response.encoding = self.charset
			if len(response.text) == 0:
				return None
			else:
				return response.text
		except Exception as e:
			print 'get_html_content(%s) error: %s' % (self.url, e)
			return None