#!/usr/bin/python
# -*- coding: utf-8 -*-
import lxml
from lxml import etree
import time

class Analysis(object):

	def get_new_datalist(self, html_doc, web_name):
		if html_doc is None or web_name is None:
			return []
		if web_name == 'qqyewu':
			return self.get_qqyewu_datalist(html_doc)
		elif web_name == 'aishoujizy':
			return self.get_aishoujizy_datalist(html_doc)
		return []

	def get_qqyewu_datalist(self, html_doc):
		url_rule = '/%s/%s' % (time.strftime('%Y', time.localtime()),time.strftime('%Y%m%d', time.localtime()))
		# url_rule = '/2019/20190902'
		html = lxml.etree.HTML(html_doc)
		a = html.xpath('//a')
		listdata = []
		for item in a:
			if item is not None:
				subject = item.attrib.get('title')
				url = item.attrib.get('href')
				if subject is not None and url.find(url_rule) > 0:
					listdata.append({'subject':subject, 'url':'http://www.qqyewu.com%s' % url})
		return listdata

	def get_detaildata(self, html_doc, url, charset='utf-8'):
		if html_doc is None or url is None:
			return []
		if url.find('qqyewu') >= 0:
			return self.get_qqyewu_detail(html_doc, url, charset)
		elif url.find('aishoujizy') >= 0:
			return self.get_aishoujizy_detail(html_doc, url, charset)
		return []

	def get_qqyewu_detail(self, html_doc, url, charset):
		html = lxml.etree.HTML(html_doc)
		data = {}
		try:
			data['catyname'] = html.xpath('/html/body/div[2]/div[2]/a[3]')[0].text
			if url.find('article') > 0:
				data['title'] = html.xpath('/html/body/div[3]/div[1]/div[1]/div[1]/div[1]/h1')[0].text
				data['content'] = html.xpath('/html/body/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]')[0]
				data['content'] = etree.tostring(data['content'],encoding=charset)
			else:
				data['title'] = html.xpath('//h1')[0].text
				data['content'] = html.xpath('//div[@class="des"]')[0]
				data['content'] = etree.tostring(data['content'],encoding=charset)
				data['downloader'] = html.xpath('//div[@class="DownloadSfotCon download"]/ul/li[1]/a')[0].attrib.get('href')
			data['content'] = data['content'].replace("<?xml version='1.0' encoding='gb2312'?>", ' ').replace("&#13;", ' ')
			data['content'] = data['content'].decode('gbk').encode('utf-8')
			return data
		except Exception as e:
			print 'Analysis detail(%s) error: %s' % (url, e)
			return None

	def get_aishoujizy_datalist(self, html_doc):
		html = lxml.etree.HTML(html_doc)
		result = html.xpath('//*[@class="lbbt_c00"]/span[@style="color: #F00;"]/following-sibling::a[1]')
		listdata = []
		for res in result:
			subject = res.attrib.get('title')
			url = 'http://www.aishoujizy.com%s' % res.attrib.get('href')
			listdata.append({'subject':url, 'url':url})
		return listdata

	def get_aishoujizy_detail(self, html_doc, url, charset):
		html = lxml.etree.HTML(html_doc)
		data = {}
		try:
			data['catyname'] = html.xpath('//*[@id="bulletin"]/a[2]')[0].text
			data['title'] = html.xpath('//*[@id="content-main"]/div[1]/div[1]/div[1]/div[1]/h2')[0].text
			content = html.xpath('//*[@id="arctext"]')[0]
			data['content'] = etree.tostring(content,encoding=charset)
			downloader = html.xpath('//*[@class="sbtn"]')
			if len(downloader) > 0:
				data['downloader'] = downloader[0].attrib.get('onclick').replace("window.open('", "").replace("');return false;", "")
				onclick = 'onclick="%s"' % downloader[0].attrib.get('onclick')
			else:
				onclick = ' '
			data['content'] = data['content'].replace("<?xml version='1.0' encoding='gb2312'?>", ' ').replace("&#13;", ' ')
			data['content'] = data['content'].decode(charset).encode('utf-8')
			downhtml = content.xpath('//*[@class="tit"]')
			if len(downhtml):
				downhtml = downhtml[0]
				downhtml = etree.tostring(downhtml,encoding=charset).replace("<?xml version='1.0' encoding='gb2312'?>", ' ').replace("&#13;", ' ').decode(charset).encode('utf-8')
				data['content'] = data['content'].replace(downhtml, " ")

			a_down = content.xpath('//*[@href="#down"]')
			for a in a_down:
				donwloaderName = lxml.etree.HTML(etree.tostring(a).replace('<i class="ico"/><i class="line"/>', "").replace('&#160;&#13;', " ")).xpath('//a')[0].text.encode('utf-8')
				onclick = a.attrib.get('onclick')
				data['content'] = data['content'].replace(donwloaderName, " ")
				data['content'] = data['content'].replace(onclick, " ")
				data['content'] = data['content'].replace('<i class="ico"/><i class="line"/>', " ")
				data['content'] = data['content'].replace('<a href="#down" onclick=" " class="sbtn" title="">  </a>', " ")
			data['content'] = data['content'].replace("font-family:'Microsoft YaHei';", " ")

			img_as = content.xpath('//*[@class="pics"]')
			for img_a in img_as:
				src = "http://www.aishoujizy.com%s" % img_a.attrib.get('href')
				a_html = '<a class="pics" href="%s" rel="pics"><img src="/images/loading.gif" class="scrollLoading" data-url="%s" alt=""/></a>' % (img_a.attrib.get('href'), img_a.attrib.get('href'))
				img = '<img src="%s" />' % src
				data['content'] = data['content'].replace(a_html, img)
			if len(downloader) > 0:
				data['content'] = '%s</div>' % data['content']
			return data
		except Exception as e:
			print 'Analysis detail aishoujizy(%s) error: %s' % (url, e)
			return None
		