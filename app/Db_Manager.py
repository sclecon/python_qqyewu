#!/usr/bin/python
# -*- coding: utf-8 -*-
import DiyMysql_Manager
import time
import jieba
import Config_Manager

class Db(object):

	def __init__(self):
		super(Db, self).__init__()
		self.DiyMysql = DiyMysql_Manager.DiyMysql()
		self.Config = Config_Manager.Config()

	def get_target_webs(self):
		db_webs = self.DiyMysql.fetch_all('target_webs', 'status = 1', 'url,charset,identifying,status')
		return_webs = []
		if len(db_webs) > 0:
			for web in db_webs:
				return_webs.append(web)
		return return_webs

	def check_newdata(self, datalist):
		if type(datalist) is not list or len(datalist) == 0:
			return []
		where_string = ''
		for item in datalist:
			if len(where_string) == 0:
				where_string += "'%s'" % item['url']
			else:
				where_string += ",'%s'" % item['url']
		where_string = 'url in (%s)' % where_string
		newlist = self.DiyMysql.fetch_all('web_urls', where_string, 'url')
		dblist = []
		for item in newlist:
			dblist.append(item[0])
		successlist = []
		for item in datalist:
			if item['url'] not in dblist and item not in successlist:
				successlist.append(item)
		return successlist

	def insert_article(self, data):
		try:
			if type(data['title']) is unicode:
				data['title'] = data['title'].encode('utf-8')
			insertData = {}
			insertData['subject'] = data['title']
			insertData['cid'] = self.getCatyId(data['catyname'])
			insertData['keywords'] = self.getKeywords(data['title'])
			insertData['description'] = self.getDescription(data['title'])
			insertData['body'] = self.getBody(data['content'])
			insertData['keywords'] = insertData['keywords'].encode('utf-8')
		except Exception as e:
			print 'insert_article keys error'
			return None
		try:
			insertData['downloader'] = self.getDownloader(data['downloader'])
		except Exception as e:
			insertData['downloader'] = ''
		insertData['dateline'] = int(time.time())

		if self.Config.is_debug() == 'insert_article':
			print ""
			print "==========debug========"
			print 'subject is type:%s' % type(insertData['subject'])
			print 'cid is type:%s' % type(insertData['cid'])
			print 'keywords is type:%s' % type(insertData['keywords'])
			print 'description is type:%s' % type(insertData['description'])
			print 'body is type:%s' % type(insertData['body'])
			exit()

		return self.DiyMysql.insert('article', insertData)

	def getCatyId(self, catyname):
		caty = self.DiyMysql.fetch_all('caty', False, 'name,isdefault,catynames,id')
		if caty is None or catyname is None:
			print 'code error: not get caty mysql infos'
			exit()
		else:
			default_catyid = None
			for item in caty:
				name = item[0]
				isdefault = item[1]
				catynames = item[2]
				catyid = item[3]
				
				if name == catyname:
					return catyid
				elif catynames.find(catyname) >= 0:
					return catyid
				elif int(isdefault) == 1:
					default_catyid = catyid
			return default_catyid

		
	def getKeywords(self, subject):
		if subject is None:
			return ''
		seg_list = jieba.cut_for_search(subject)
		return ",".join(seg_list)
		
	def getDescription(self, subject):
		return subject
		
	def getBody(self, body):
		return body
		
	def getDownloader(self, downloader):
		if len(downloader) == 0:
			return ''
		downloader = "点击下载|%s" % downloader.encode('utf-8')
		return downloader

	def insert_webs(self, data, typeinfo):
		try:
			insertData = {}
			insertData['url'] = data['url']
			insertData['name'] = data['subject']
			insertData['type'] = typeinfo
			insertData['dateline'] = int(time.time())
		except Exception as e:
			return None
		return self.DiyMysql.insert('web_urls', insertData)

		