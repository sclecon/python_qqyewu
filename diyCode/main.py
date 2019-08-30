#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import web_manager
import analysis_manager
import url_manager
import diymysql_manager

if __name__ == '__main__':
	web_manager = web_manager.web_manager()
	analysis_manager = analysis_manager.analysis_manager()
	url_manager = url_manager.url_manager()
	DIyMysqlDB = diymysql_manager.DIyMysqlDB()

	root_url = 'http://www.qqyewu.com'
	
	nowtime = int(time.time())
	
	dgetime = 5
	
	runNum = 0
	
	runMaxNum = '*'
	
	while True:
		runtime = int(time.time())
		
		if runtime > (nowtime+dgetime):
			runNum+=1
			nowtime = int(time.time())
			roothtml = web_manager.get_html(root_url)
			if roothtml is None:
				print '第%d次监测:获取数据失败' % runNum
				print ""
				continue
			else:
				print '第%d次监测:获取数据成功' % runNum
			rootData = analysis_manager.analysis_nowurls(roothtml, root_url)
			
			if len(rootData['url']) == 0:
				print '没有获取到新数据'
				print ""
				continue
			elif url_manager.is_notget(rootData['url']) is None:
				print '没有最新的数据了'
				print ""
				continue
			else:
				print '有新数据'
				geturls = url_manager.is_notget(rootData['url'])
			successNum = 0
			for url in geturls:
				itemhtml = web_manager.get_html(url)
				itemdata = analysis_manager.DetailData(itemhtml, url)
				try:
					downloader = itemdata['downloader']
				except Exception as e:
					downloader = ''
				if DIyMysqlDB.addArticle(itemdata['catyname'], itemdata['title'], itemdata['body'], downloader) is not None:
					url_manager.add_successUrl(url)
					print '写入 %s 的数据成功' % url
				else:
					print '写入 %s 的数据失败' % url
		if runNum > runMaxNum and runMaxNum is not "*":
			print '监测结束'
			break