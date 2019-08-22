#!/usr/bin/python
# -*- coding: utf-8 -*-


if __name__ == '__main__':
	root_url = 'http://www.qqyewu.com'
	url_manager.add_url(root_url)
	errorNum = 0
	successNum = 0
	while url_manager.is_newurl():
		itemurl = url_manager.get_newurl()
		itemhtml,itemcode = web_manager.get_html(itemurl)
		if itemcode != 200:
			print 'error:%s' % itemurl
			if errorNum > 10:
				break
			else:
				errorNum+=1
		else:
			# itemdata = html_manager.get_data(itemhtml)
			# print itemdata
			newurls = html_manager.get_newurl(itemhtml)
			if newurls:
				print newurls
				successNum+=1
				
				if successNum > 10:
					break
	