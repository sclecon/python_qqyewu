#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib


class web_manager(object):
	def get_html(self, url):
		if url is None:
			return None
		response = urllib.urlopen(url)
		if response.getcode() == 200:
			return response.read()
		else:
			return None