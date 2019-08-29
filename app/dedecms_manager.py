#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb
import time

class DedeCMS(object):
	dedeCaty = {89:['QQ资讯','QQ新闻资讯','QQ急救室','免费QQ业务','免费QQ秀','免费点亮QQ图标'], 84:['QQ新闻','QQ空间代码','QQ空间模块','QQ常见问题'], 85:['QQ教程'], 91:['QQ软件'], 92:['更多资讯'], 90:['网赚笔记'], 86:['值得一看','游戏攻略','网游攻略'], 87:['剁手党','天天剁手价'], 88:['网站公告']}
	default_typeid = 92
	
	def insert(self, data):
		if data is None:
			return None
		try:
			if data['url_type'] is None:
				data['url_type'] = 'article'
		except:
			data['url_type'] = 'article'
		try:
			if data['catyname'] is None:
				data['catyname'] = '活动线报'
		except:
			data['catyname'] = '活动线报'
		try:
			if data['keyword'] is None:
				data['keyword'] = 'keyword'
		except:
			data['keyword'] = 'keyword'
		try:
			if data['description'] is None:
				data['description'] = 'description'
		except:
			data['description'] = 'description'
		try:
			if data['downloader'] is None:
				data['downloader'] = 0
		except:
			data['downloader'] = 0
		try:
			if data['downname'] is None:
				data['downname'] = '点击下载'
		except:
			data['downname'] = '点击下载'
		data['typeid'] = self.get_newdata_type(data['catyname'])
		
		if data['url_type'] == 'article':
			aid = self.add_article(data['typeid'], data['title'], data['body'])
		else:
			aid = self.add_soft(data['typeid'], data['title'], data['body'], data['downloader'], data['downname'])
		# print aid
		return True
	
	def get_newdata_type(self, catyname):
		typeid = self.default_typeid
		if catyname is None:
			return typeid
		print catyname
		for item_typeid,types in self.dedeCaty.items():
			if catyname in types:
				typeid = item_typeid
		return typeid
	
	def add_article(self, typeid, title, body, keyword='', description=''):
		addIntTime = int(time.time())
		aid = self.GetIndexKey(typeid,1);
		
		common_sql = "insert dede_archives (`id`,`typeid`,`sortrank`,`flag`,`ismake`,`click`,`title`,`shorttitle`,`color`,`writer`,`source`,`litpic`,`pubdate`,`senddate`,`mid`,`keywords`,`description`,`dutyadmin`,`voteid`) values \
		('%s','%s','%s','','1','100','%s','%s','','管理员','未知','','%s','%s','1','%s','%s','1','0')" % (aid, typeid, addIntTime, title, title, addIntTime, addIntTime, keyword, description)
		article_sql = "insert dede_addonarticle (`aid`,`typeid`,`body`,`redirecturl`,`templet`,`userip`,`flash`) values ('%s','%s','%s','','','127.0.0.1','')" % (aid,typeid,body)
		conn = self.mysqlConn()
		cur = conn.cursor()
		try:
			cur.execute(common_sql)
			cur.execute(article_sql)
			return aid
		except Exception as e:
			conn.rollback()
			print 'callback: %s' % e
		finally:
			conn.close()
		return None
	
	def add_soft(self, typeid, title, body, downloader, downname, keyword='', description=''):
		addIntTime = int(time.time())
		aid = self.GetIndexKey(typeid,3);
		common_sql = "insert dede_archives (`id`,`typeid`,`sortrank`,`flag`,`ismake`,`click`,`title`,`shorttitle`,`color`,`writer`,`source`,`litpic`,`pubdate`,`senddate`,`mid`,`keywords`,`description`,`dutyadmin`,`voteid`,`channel`) values \
		('%s','%s','%s','','3','100','%s','%s','','管理员','未知','','%s','%s','1','%s','%s','1','0','3')" % (aid, typeid, addIntTime, title, title, addIntTime, addIntTime, keyword, description)
		softlinks = "{dede:link text='%s'} %s {/dede:link}" % (downname,downloader)
		soft_sql = "insert dede_addonsoft (`aid`,`typeid`,`filetype`,`language`,`softtype`,`accredit`,`os`,`softrank`,`officialUrl`,`officialDemo`,`softsize`,`softlinks`,`introduce`,`daccess`,`needmoney`,`templet`,`userip`,`redirecturl`,`flash`) values ('%s','%s','.exe','简体中文','国产软件','共享软件','Win2003,WinXP,Win2000,Win9X','3','http://','http://','20 MB',\"%s\",'%s','0','0','','127.0.0.1','','')" % (aid,typeid,softlinks,body)
		# return soft_sql
		conn = self.mysqlConn()
		cur = conn.cursor()
		try:
			cur.execute(common_sql)
			cur.execute(soft_sql)
			return aid
		except Exception as e:
			conn.rollback()
			print 'callback: %s' % e
		finally:
			conn.close()
		return None
	
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
			port=3306,
			charset='gbk'
		)
		return db


	def GetIndexKey(self, typeid, channel=1):
		conn = self.mysqlConn()
		cur = conn.cursor()
		sql = "insert into dede_arctiny(typeid,mid,senddate,sortrank,channel) values ('%d','1','%d','%d','%d')" % (typeid,int(time.time()),int(time.time()),channel)
		try:
			cur.execute(sql)
			aid = conn.insert_id()
			conn.commit()
			return aid
		except Exception as e:
			conn.rollback()
		finally:
			conn.close()
	

if False:
	title = "测试帖子 QQ教程 更新缓存 时间：%s" % time.strftime('%Y-%m-%d', time.localtime())
	DedeData = {'catyname':'QQ教程', 'url_type':'sort', 'title':title, 'body':'body message python测试添加内容','downloader':'http://www.baidu.com','downname':'百度下载'}
	if DedeCMS().insert(DedeData) is True:
		print '插入数据成功'
	else:
		print '插入数据失败'