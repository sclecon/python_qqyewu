#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb
import time

class DedeCMS(object):
	
	def insert(self, data):
		if data is None:
			return None
		try:
			if data['url_type'] is None:
				data['url_type'] = 'article'
		except:
			data['url_type'] = 'article'
		IndexData = self.get_newdata_type(data)
		if data['url_type'] == 'article':
			sql = self.get_article_sql(data)
		else:
			sql = self.get_soft_sql(data)
		print sql
		print self.get_newdata_type(data)
		return True
	
	def get_newdata_type(self, data):
		return {'typeid': 84, 'mid':'1'}
	
	def mysqlConn(self):
		mysql_config = {
			'host':'193.112.106.192', 
			'user':'dedecms_com', 
			'pass':'dedecms_com', 
			'tablename': 'dedecms_com'
		}
		
		db = MySQLdb.connect(
			host=mysql_config['host'], 
			user=mysql_config['user'], 
			passwd=mysql_config['pass'], 
			db=mysql_config['tablename'], 
			port=3306 
		)
		return db


	def GetIndexKey(self, typeid, mid):
		conn = self.mysqlConn()
		cur = conn.cursor()
		sql = "insert into dede_arctiny(typeid,mid,senddate,sortrank) values ('%d','%d','%d','%d')" % (typeid,mid,int(time.time()),int(time.time()))
		try:
			cur.execute(sql)
			aid = conn.insert_id()
			conn.commit()
			return aid
		except Exception as e:
			conn.rollback()
		finally:
			conn.close()
	
	def AddDedecmsArchivets(self, typeid, title, keyword='keyword', description='description', body='bodyText', downurl=0, downname=0):
		addIntTime = int(time.time())
		aid = self.GetIndexKey(typeid,1);
		sql = "insert into dede_archives(\
		id,\
		title,\
		description,\
		voteid,\
		sortrank,\
		flag,\
		ismake,\
		channel,\
		writer,\
		source,\
		litpic,\
		pubdate,\
		senddate,\
		mid,\
		dutyadmin,\
		weight,\
		keywords\
		) values (\
		'%d','%s','%s',0,'%d','p',1,3,'Admin','weizhi','','%d','%d',1,1,'%d','%s'\
		);" % (
			aid,
			title, 
			description,
			addIntTime,
			addIntTime,
			addIntTime,
			aid,
			keyword
		)
		if downurl != 0 and downname != 0:
			downBt = "{dede:link text=\\\'%s\\\'} %s {/dede:link}" % (downname, downurl)
			addonsql = "insert into dede_addonsoft(aid,typeid,filetype,language,softtype,accredit,os,softrank,officialUrl,officialDemo,softsize,softlinks,introduce,daccess,needmoney,userip,templet,redirecturl,flash) values \
			('%d','%d','.exe','系统软件','国产软件','国产软件','Win2003,WinXP,Win2000,Win9X','3','http://','http://','国产软件','%s','%s',0,0,'127.0.0.1','','','');" % (aid,typeid,downBt,body);
		else:
			addonsql = "insert into dede_addonarticle(aid,typeid,body,redirecturl,templet,userip,flash,ywurl,youhuiurl) values \
			('%d','%d','%s','','','127.0.0.1','','','');" % (aid,typeid,body);
			print addonsql
			print ''
			print ''
		# return addonsql
		sql += addonsql

		# return sql
		conn = self.mysqlConn()
		cur = conn.cursor()
		try:
			cur.execute(sql)
			return aid
		except Exception as e:
			conn.rollback()
			print 'callback'
		finally:
			conn.close()

# INSERT INTO `dedecms_com`.`dede_arctiny` (`id`, `typeid`, `typeid2`, `arcrank`, `channel`, `senddate`, `sortrank`, `mid`) VALUES (NULL, '85', '0', '0', '1', '1566463017', '1566463017', '1');
# INSERT INTO `dedecms_com`.`dede_archives` (`id`, `typeid`, `typeid2`, `sortrank`, `flag`, `ismake`, `channel`, `arcrank`, `click`, `money`, `title`, `shorttitle`, `color`, `writer`, `source`, `litpic`, `pubdate`, `senddate`, `mid`, `keywords`, `lastpost`, `scores`, `goodpost`, `badpost`, `voteid`, `notpost`, `description`, `filename`, `dutyadmin`, `tackid`, `mtype`, `weight`) VALUES ('1200', '85', '0', '1566463017', NULL, '1', '3', '0', '0', '0', '文章标题信息', '', '', '管理员', '未知', NULL, '1566463017', '1566463017', '1', '关键词', '0', '0', '0', '0', '0', '0', '网站的SEO描述信息', '', '0', '0', '0', '1103');
# INSERT INTO `dedecms_com`.`dede_addonarticle` (`aid`, `typeid`, `body`, `redirecturl`, `templet`, `userip`, `flash`, `ywurl`, `youhuiurl`) VALUES ('1200', '85', '内容主题内容', '', '', '127.0.0.1', '', NULL, NULL);


DedeData = {}
if DedeCMS().insert(DedeData) is True:
	print '插入数据成功'
else:
	print '插入数据失败'