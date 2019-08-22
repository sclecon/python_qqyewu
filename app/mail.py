#!/usr/bin/python
# -*- coding: utf-8 -*-
import time,web_manager,analysis_manager

if __name__ == '__main__':
	# 定义模块
	web_manager = web_manager.web_manager()
	analysis_manager = analysis_manager.analysis_manager()

	# 监测网址
	root_url = 'http://www.qqyewu.com'
	
	# 获取当前时间戳
	nowtime = int(time.time())
	
	# 监控每次请求的间隔时间
	dgetime = 0.1
	
	# 当前监测次数
	runNum = 0
	
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
			print rootData
			break
			# 判断分析出的目标数据是否存在新数据
			
			
			# 循环判断是否已经获取过
			
			
			# 循环获取新数据详细内容
			
			
			# 获取当前新数据详细内容中的指定数据
			
			
			# 记录当前获取到的数据
			
			
			# 记录当前获取的数据网址
			
		if runNum > 100:
			break