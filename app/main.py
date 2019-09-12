#!/usr/bin/python
# -*- coding: utf-8 -*-
import Db_Manager
import Request_Manager
import Analysis_Manager
import DiyMysql_Manager

class General_Manager(object):

	def __init__(self):
		super(General_Manager, self).__init__()
		self.Db = Db_Manager.Db()
		self.Request = Request_Manager.Request()
		self.Analysis = Analysis_Manager.Analysis()
		self.DiyMysql = DiyMysql_Manager.DiyMysql()

	def start(self):
		webs = self.Db.get_target_webs()
		for web in webs:
			self.Request.set_rooturl(web[0])
			self.Request.set_charset(web[1])
			root_html = self.Request.get_html_content()
			if root_html is None:
				continue
			new_datalist = self.Analysis.get_new_datalist(root_html, web[2])
			if len(new_datalist) == 0:
				print '%s not is new data(gethtml)' % web[0]
				continue
			successdata = self.Db.check_newdata(new_datalist)
			if len(successdata) == 0:
				print '%s not is new data(\'sql\')' % web[0]
				continue
			for item in successdata:
				url = item['url']
				subject = item['subject']
				html_doc = self.Request.get_html_content(url)
				data = self.Analysis.get_detaildata(html_doc, url, web[1])
				if data is not None:
					result = self.Db.insert_article(data)
					if result:
						res = self.Db.insert_webs(item, web[2])
					else:
						res = False

					if res is not False and res is not None:
						print 'data insert success : %s' % url
					else:
						print 'data insert error : %s' % url
					print ""
					print ""
					print ""







		

if __name__ == '__main__':
	General_Manager = General_Manager()
	General_Manager.start()