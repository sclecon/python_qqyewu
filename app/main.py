#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import web_manager
import analysis_manager
import url_manager
import dedecms_manager

if __name__ == '__main__':
	# 定义模块
	web_manager = web_manager.web_manager()
	analysis_manager = analysis_manager.analysis_manager()
	url_manager = url_manager.url_manager()
	DedeCMS = dedecms_manager.DedeCMS()

	# 监测网址
	root_url = 'http://www.qqyewu.com'
	
	# 获取当前时间戳
	nowtime = int(time.time())
	
	# 监控每次请求的间隔时间
	dgetime = 5
	
	# 当前监测次数
	runNum = 0
	
	# 定义监测最大次数 *=无限次
	runMaxNum = 10000
	
	# 循环监测
	while True:
		runtime = int(time.time())
		
		# 判断是否已经过了每次监测等待时间
		if runtime > (nowtime+dgetime):
			# 记录这是第多少次监测
			runNum+=1
			
			# 设置本次监测时间
			nowtime = int(time.time())
			
			# 获取监测目标数据
			roothtml = web_manager.get_html(root_url)
			
			# 判断获取监测目标数据是否成功
			if roothtml is None:
				print '第%d次监测:获取数据失败' % runNum
				continue
			else:
				print '第%d次监测:获取数据成功' % runNum
			# 分析监测目标数据
			rootData = analysis_manager.analysis_nowurls(roothtml, root_url)
			# print rootData
			
			# 判断分析出的目标数据是否存在新数据
			if len(rootData['url']) == 0:
				print '没有获取到新数据'
				continue
			elif url_manager.is_notget(rootData['url']) is None:
				print '没有最新的数据了'
				continue
			else:
				geturls = url_manager.is_notget(rootData['url'])
				print geturls
				# break
			# 循环获取新数据详细内容
			for url in geturls:
				# 获取详情页的html
				itemhtml = web_manager.get_html(url)
				# 解析详情页数据
				itemdata = analysis_manager.DetailData(itemhtml, url)
				# 打印一下详情页数据
				print url
				print itemdata['title']
				# print itemdata['body']
				print itemdata
				print ""
				print ""
				# 将采集到的数据发送到dedecms
				if DedeCMS.insert(itemdata) is not None:
					# 将当前的url保存到已采集列表
					url_manager.add_successUrl(url)
		if runNum > runMaxNum and runMaxNum is not "*":
			break