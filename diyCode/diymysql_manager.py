#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import MySQLdb
import json
import chardet
import jieba
import sys
if sys.getdefaultencoding() != 'gbk':
    reload(sys)
    sys.setdefaultencoding('gbk')

class DIyMysqlDB(object):
	
	MysqlConfig = {
			'host':'193.112.106.192', 
			'user':'diymysql', 
			'pass':'diymysql', 
			'tablename': 'diymysql',
			'charset': 'utf8',
			'port': 3306
		}
	
	def mysqlConn(self):
		
		try:
			conn = MySQLdb.connect(
				host=self.MysqlConfig['host'], 
				user=self.MysqlConfig['user'], 
				passwd=self.MysqlConfig['pass'], 
				db=self.MysqlConfig['tablename'], 
				port=self.MysqlConfig['port'],
				charset=self.MysqlConfig['charset'],
			)
		except Exception as e:
			print '程序终止：数据库链接错误: %s' % e
			exit()
		return conn
	
	def getCatyId(self, catyname):
		conn = self.mysqlConn()
		try:
			cursor = conn.cursor()
			cursor.execute('SELECT name,isdefault,catynames,id from caty order by id desc')
			caty = cursor.fetchall()
		except Exception as e:
			conn.close()
			print '程序终止：获取数据库分类出错: %s' % e
			exit()
		conn.close()
		if caty is None or catyname is None:
			print '程序终止：未获取到数据库分类或未获取到传入分类名称，请检查！'
			exit()
		else:
			default_catyid = None
			catyname = catyname.decode('gbk')
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
	
	def addArticle(self, catyname, subject, body, downloader=''):
		data = {}
		data['subject'] = subject
		data['cid'] = self.getCatyId(catyname)
		data['keywords'] = self.getKeywords(subject)
		data['description'] = self.getDescription(subject)
		data['body'] = self.getBody(body)
		data['downloader'] = self.getDownloader(downloader)
		data['dateline'] = int(time.time())
		return self.insertData('article', data)
		
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
		json = "点击下载|%s" % downloader
		return json.decode('gbk')
		
	def insertData(self, table, data={}):
		if type(data) is not dict or table is None or len(table) == 0:
			return None
		field = ''
		value = ''
		for k,v in data.items():
			if len(field) == 0:
				field = '`%s`' % k
			else:
				field += ',`%s`' % k
			# print k
			# print v
			# print type(v)
			# print '==========================================='
			if len(value) == 0:
				value = '"%s"' % v
			else:
				value += ',"%s"' % v
		sql = 'insert %s (%s) values (%s)' % (table, field, value)
		conn = self.mysqlConn()
		cur = conn.cursor()
		aid = None
		try:
			cur.execute(sql)
			aid = conn.insert_id()
			conn.commit()
		except Exception as e:
			print "写入数据到数据库错误:%s" % e 
			conn.rollback()
		finally:
			conn.close()
		return aid