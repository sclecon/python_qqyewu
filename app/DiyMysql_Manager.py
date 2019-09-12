#!/usr/bin/python
# -*- coding: utf-8 -*-
import Config_Manager
import MySQLdb

class DiyMysql(object):
	mysql_conn = None

	def __init__(self):
		super(DiyMysql, self).__init__()
		self.Config = Config_Manager.Config()

	def get_mysql_cursor(self):
		MysqlConfig = self.Config.get_mysql_config()
		if MysqlConfig is None:
			return None
		try:
			conn = MySQLdb.connect(
				host=MysqlConfig['host'], 
				user=MysqlConfig['user'], 
				passwd=MysqlConfig['pass'], 
				db=MysqlConfig['db'], 
				port=MysqlConfig['port'],
				charset=MysqlConfig['charset'],
			)
		except Exception as e:
			print 'mysql connect error: %s' % e
			exit()
		self.mysql_conn = conn
		return self.mysql_conn.cursor()

	def close_mysql(self):
		if self.mysql_conn is not None:
			self.mysql_conn.close()
			self.mysql_conn = None

	def rollback_mysql(self):
		if self.mysql_conn is not None:
			self.mysql_conn.rollback()

	def fetch_all(self, table, where=False, field='*', limit=False):
		if field is None or table is None:
			return {}
		append_string = ''
		if where is not False:
			append_string += 'where %s ' % where
		if limit is not False:
			append_string += 'limit %s' % limit
		sql = """select %s from %s %s""" % (field, table, append_string)
		try:
			cursor = self.get_mysql_cursor()
			cursor.execute(sql)
			data = cursor.fetchall()
			if len(data) == 1 and limit is not False:
				return data[0]
			else:
				return data
		except Exception as e:
			print 'run sql error: %s and sql = %s' % (e,sql)
			self.rollback_mysql()
			exit()
		finally:
			self.close_mysql()

	def find(self, table, where=False, field='*'):
		return self.fetch_all(table, where, field, 1)

	def insert(self, table, data={}):
		if type(data) is not dict or table is None or len(table) == 0:
			return None
		field = ''
		value = ''
		for k,v in data.items():
			if len(field) == 0:
				field = '`%s`' % k
			else:
				field += ',`%s`' % k
			if len(value) == 0:
				value = "'%s'" % v
			else:
				value += ",'%s'" % v
		sql = 'insert into `%s` (%s) values (%s)' % (table, field, value)
		if self.Config.is_debug() == 'insert':
			print sql
			exit()
		try:
			cursor = self.get_mysql_cursor()
			cursor.execute(sql)
			insert_id = self.mysql_conn.insert_id()
			self.mysql_conn.commit()
			if insert_id:
				return insert_id
			else:
				return False
		except Exception as e:
			print "insert db error:%s " % e 
			print ""
			print ""
			print data['subject']
			print type(data['subject'])
			print ""
			print ""
			print sql
			print ""
			self.rollback_mysql()
			exit()
		finally:
			self.close_mysql()

	def update(self, table, data, where=False):
		if table is None or type(data) is not dict:
			return None
		where_string = ''
		if where is not False:
			where_string += 'where %s' % where
		data_string = ''
		for k,v in data.items():
			if len(data_string) == 0:
				data_string += "`%s`='%s'" % (k,v)
			else:
				data_string += ",`%s`='%s'" % (k,v)
		if len(data_string) == 0:
			return None
		sql = 'update `%s` set %s %s' % (table, data_string, where_string)
		try:
			cursor = self.get_mysql_cursor()
			cursor.execute(sql)
			return True
		except Exception as e:
			print "update db error:%s " % e 
			self.rollback_mysql()
			exit()
		finally:
			self.close_mysql()

	def delete(self, table, where=False):
		if table is None or where is None:
			return None
		where_string = ''
		if where is not False:
			where_string += 'where %s' % where
		sql = 'delete from `%s` %s' % where_string
		try:
			cursor = self.get_mysql_cursor()
			cursor.execute(sql)
			self.mysql_conn.commit()
			return True
		except Exception as e:
			print "delete error:%s " % e 
			self.rollback_mysql()
			exit()
		finally:
			self.close_mysql()
