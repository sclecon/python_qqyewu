#!/usr/bin/python
# -*- coding: utf-8 -*-

class url_manager(object):
	
	urlsisok = set()
	
	def is_notget(self, urls):
		if urls is None:
			return None
		notget = []
		for url in urls:
			if url not in self.urlsisok:
				notget.append(url)
		return notget
	
	def add_successUrl(self, url)
		if url is None:
			return None
		if url not in self.urlsisok:
			self.urlsisok.append(url)
		return True