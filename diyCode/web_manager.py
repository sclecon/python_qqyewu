#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import requests
import time


class web_manager(object):
	def get_html(self, url):
		if url is None:
			return None
		response = urllib.urlopen(url)
		if response.getcode() == 200:
			return response.read()
		else:
			return None
	def updateHtmlCache(self, starttime=None):
		
		# config data
		url_host = 'http://193.112.106.192:2222/dede/makehtml_all.php'
		headers={
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
			"Cookie":"menuitems=1_1%2C2_1%2C3_1%2C4_1%2C5_1%2C6_1; PHPSESSID=60por3j33b2kr56qv5v9rbi55i; userinfo=c8ae438aa5c771d91317f09cdbbe7dc5cc5f4643e76c1c1f72e4e3532e701ced7ce3a7e8f408fa4b309ed683ed40300022823073e009c57bb5680653796da17dda0b2b6e59793029bd333183978605acea1caa9ed24dd718069d8dd1cb729cb605e22679d9ed3fd44bebbbc661bbc86b1c5544ed326142f1e4a48413ae084ea87f3a2e5a08115654421ad4c3c5694b5908a8657c7d86e367825001318fffd0ece80d78acd970e69ab770ffad7a32f33868a6fb9f47332943bab0d39420761007; UM_distinctid=16cd606099c2b0-099d50cd6d6f32-7373e61-1fa400-16cd606099d2a1; __51cke__=; Hm_lvt_d4719441919bf7f420aaf4ba7445a99f=1566199259,1566810494,1566958832; lastCid=88; lastCid__ckMd5=85b8a7cbc923e3a5; DedeUserID=1; DedeUserID__ckMd5=54b7b712ddff097a; DedeLoginTime=1566977332; DedeLoginTime__ckMd5=159b237bed9d8383; __tins__19731659=%7B%22sid%22%3A%201566983430439%2C%20%22vd%22%3A%206%2C%20%22expires%22%3A%201566985267749%7D; __51laig__=70; Hm_lpvt_d4719441919bf7f420aaf4ba7445a99f=1566983468; CNZZDATA1274394511=1826347563-1566953917-%7C1567059400; _csrf_name_42c4f278=b1d82854faf2228f61878823ce52ed65; _csrf_name_42c4f278__ckMd5=6b7a1260f30e697b; ENV_GOBACK_URL=%2Fdede%2Fcontent_list.php%3Fdopost%3DlistArchives%26keyword%3D%26cid%3D0%26flag%3D%26orderby%3Did%26arcrank%3D%26channelid%3D0%26f%3Dform1.arcid1%26totalresult%3D64%26pageno%3D1"
		}
		
		try:
			if starttime is None:
				starttime = time.strftime('%Y-%m-%d', time.localtime())
			timeStamp =  int(time.mktime(time.strptime("%s 00:00:00" % starttime, "%Y-%m-%d %H:%M:%S")))+(3600*24)
			session = requests.session()
			nowtime = int(time.time())
			ingtime = 1
			start = 1
			over = 5
			while start <= over:
				if nowtime+ingtime < int(time.time()):
					if start == 1:
						post_data = {"action":"make", "uptype":"time", "starttime":starttime, "startid":"0","Submit":"开始更新"}
						html = session.post(url_host, data=post_data, headers=headers)
						# print html.content
					elif start > 1 and start < 5:
						get_url = "%s?action=make&step=%s&uptype=time&mkvalue=%s" % (url_host, start, timeStamp)
						html = session.get(get_url, headers=headers)
						# print html.content
					else:
						get_url = "%s?action=make&step=10" % (url_host)
						html = session.get(get_url, headers=headers)
						# print html.content
					start+=1
					nowtime = int(time.time())
		except Exception as e:
			print "error: %s" % e
			return False
		return True

if False:
	if web_manager().updateHtmlCache(time.strftime('%Y-%m-%d', time.localtime())):
		print "更新缓存成功"
	else:
		print "更新缓存失败"