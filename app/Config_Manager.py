#!/usr/bin/python
# -*- coding: utf-8 -*-

class Config(object):

	mysql_config = {}
	debug = False

	def get_mysql_config(self):
		default_config = {
				'host':'127.0.0.1',
				'user':'root',
				'pass':'root',
				'db':'root',
				'charset':'utf8',
				'port':3306
			}
		if self.mysql_config is None:
			return default_config
		for k,v in default_config.items():
			try:
				if self.mysql_config[k] is not None:
					default_config[k] = self.mysql_config[k]
			except Exception as e:
				pass
		return default_config

	def is_debug(self):
		default_debug = False
		try:
			default_debug = self.debug
		except Exception as e:
			pass
		return default_debug;
		