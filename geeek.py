#coding:utf8
import urllib, urllib2
import json
import re
import os
import time
import platform
from config import *

class Geek:
	'''docstring for Geek'''
	def __init__(self, cookie, proxy = None):
		user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
		self.proxy = proxy
		self.headers = { 
			'User-Agent' : user_agent,
			'Content-Type' : 'application/json',
			'Referer' : 'https://time.geekbang.org/column/110',
			'Cookie': cookie

		}
		self.static_headers = {
			'User-Agent' : user_agent,
			'authority' : 'static001.geekbang.org',
			'method' : 'GET',
			'scheme' : 'https',
			'Range' : 'bytes=0-',
			'Referer' : 'https://static001.geekbang.org/resource/audio/f1/1c/f17bd3ea34f96b77e3cb0336b6aa3d1c.mp3',
			'Cookie': cookie
		}
		self.api = {
			'getArticles': 'https://time.geekbang.org/serv/v1/column/articles',
			'getArticleContent': 'https://time.geekbang.org/serv/v1/article',
			'getComments': 'https://time.geekbang.org/serv/v1/comments',
			'getMyList': 'https://time.geekbang.org/serv/v1/my/products/list',
		}
		self.zhuanlan_dict = {
			110: '邱跃的产品实践',
			85: '趣谈网络协议',
			143: '程序员的数学基础课',
			140: 'Linux性能优化实战',
			126: '数据结构与算法之美',
			79: '技术领导力300讲',
			42: '技术与商业案例解析',
			113: '技术管理实战36讲',
			63: '赵成的运维体系',
			81: '从0开始学架构',
			48: '左耳听风',
			80: '硅谷产品实战36讲',
			139: 'MySQL实战45讲',
			133: '从0开始学大数据',
		}


	def getAllZhuanlanList(self):
		allList = []
		prev = 0
		while True:
			ret = self.getZhuanlanListByPage(prev)
			pageList = ret.get('data').get('list')
			if pageList:
				allList.extend(pageList)
				prev = pageList[-1].get('score')
			else:
				break

		return allList


	def getZhuanlanListByPage(self, prev, size = 10):
		'''得到我订阅的专栏列表
		'''
		url = self.api.get('getMyList')
		data = {'nav_id':1, 'prev': prev, 'size': size}

		ret = self.__request(url, data)

		return ret


	def getArticles(self, cid, timestamp, limit, order = 'newest'):
		''' 得到专栏的文章列表
		@param cid 专栏id
		@param page 页码
		@param limit 页大小
		'''
		url = self.api.get('getArticles')
		data = {'cid':cid,'size':limit,'prev':timestamp,'order':order,'sample':True}

		ret = self.__request(url, data)

		return ret.get('data').get('list')


	def getArticleContent(self, article_id):
		'''得到某个专栏内容
		'''
		url = self.api.get('getArticleContent')
		data = {'id':article_id, 'include_neighbors':True}

		ret = self.__request(url, data)

		return ret.get('data')


	def getStaticResouce(self, url):
		'''静态资源获取
		'''
		return self.__request(url, headers = self.static_headers)


	def getAndSaveArticle(self, zhuanlanid, article_id):
		'''保存文章
		（1）、Windows操作系统对文件和文件夹命名限制:

			1.1) 以下字符不能出现在文件和文件夹名称中：（引号之内）

			'/'  '?'  '*'  ':'  '|'  '\'  '<'  '>'

			1.2) 以下字符不能命名为文件或文件夹的名称：（引号之内）

			"con","aux","nul","prn","com0","com1","com2","com3","com4","com5","com6","com7"

			"com8","com9","lpt0","lpt1","lpt2","lpt3","lpt4","lpt5","lpt6","lpt7","lpt8","lpt9"

			1.3) 另外，由于Windows对全文件名的字符长度作出258个字符以内的限制。全文件名长度指的是包括了文件路径的全部长度（一个汉字也按一个字符计算）。

			（2）、Linux操作系统对文件和文件夹命名限制:

			2.1) 除了 / 之外，所有的字符都合法。
			2.2) 有些字符最好不用，如空格符、制表符、退格符和字符 @ # $ & ( ) - 等。
			2.3) 避免使用加减号或 . 作为普通文件名的第一个字符。
			2.4) 大小写敏感。
			2.5) Linux 系统下的文件名长度最多可到256个字符。

			（3）、Unix操作系统对文件和文件夹命名限制：

			3.1）最多 255 个字符，除了字符 / 及空格其余均可。

			3.2) 虽然在Unix系统中可以使用一些特殊的符号作为文件或者目录的名字。但是除非有特殊的必要，最好在文件名字中不要包含特殊符号。
		'''
		art = self.getArticleContent(article_id)
		audio_download_url = art.get('audio_download_url')
		article_content = art.get('article_content')
		article_title = art.get('article_title')

		# 文件名称处理
		article_title = re.sub('[\/|\?|\*|\:|\||\\|\<|\>]', '-', article_title)
		print '%s.html' % article_title

		article_title = article_title.encode('utf8')
		self.saveContent(zhuanlanid, '%s.html' % article_title, article_content)

		if audio_download_url:
			audio = self.getStaticResouce(audio_download_url)
			geek.saveContent(zhuanlanid, '%s.mp3' % article_title, audio, False)


	def getZhuanlan(self, zhuanlanid, timestamp, limit = 20, order = 'newest'):
		'''处理一个专栏
		@param zhuanlanid 
		@param timestamp 分页拉取的上批次文章的最大或最小文章时间戳
		@param limit 分页的页大小
		@param order 排序方式 newest文章从新到旧，earliest则相反
		'''
		print 'start get zhuanlan', zhuanlanid
		while True:
			article_list = self.getArticles(zhuanlanid, timestamp, limit, order)

			if not article_list:
				break

			if timestamp > 0 and order == 'newest' and article_list[0].get('score') > timestamp:
				break

			if timestamp > 0 and order == 'earliest' and article_list[0].get('score') < timestamp:
				break

			print 'start get article'

			for article in article_list:
				timestamp = article.get('score')
				article_id = article.get('id')

				print 'article_id', article_id, 'timestamp', timestamp

				self.getAndSaveArticle(zhuanlanid, article_id)

				# 限制时间，不要太频繁请求人家的服务器啦，做人要厚道
				time.sleep(1)

		return timestamp

	def getComments(self, article_id, timestamp = 0):
		'''获取文章评论
		{"aid":"73188","prev":0}
		'''
		url = self.api.get('getComments')
		data = {'aid':article_id, 'prev':timestamp}

		ret = self.__request(url, data)

		return ret.get('data')


	def saveContent(self, zhuanlanid, file_name, content, is_text = True):
		'''保存内容到本地
		'''
		current_dir_path = os.path.dirname(os.path.realpath(__file__))

		dname = self.zhuanlan_dict.get(zhuanlanid)
		if not platform.system().lower() == 'linux':
			dname = dname.decode('utf8')
			file_name = file_name.decode('utf8')

		zhuanlanpath = os.path.join(current_dir_path, dname)
		if not os.path.exists(zhuanlanpath):
			os.mkdir(zhuanlanpath)

		file_path = os.path.join(zhuanlanpath, file_name)
		with open(file_path, 'wb') as f:
			try:
				if is_text:
					f.write(content.encode('utf8'))
				else:
					f.write(content)
				print 'save file'
			except Exception as e:
				print e, 'in saveContent'
			

	def __request(self, url, data = None, headers = None):
		'''统一请求处理
		'''
		if self.proxy:
			proxy = urllib2.ProxyHandler(self.proxy)
			opener = urllib2.build_opener(proxy)
			#定制opener
			urllib2.install_opener(opener)

		if headers is None:
			headers = self.headers

		if data is not None:
			request = urllib2.Request(url, json.dumps(data), headers)
		else:
			request = urllib2.Request(url, headers = headers)

		response = urllib2.urlopen(request) 
		ret = response.read()

		try:
			ret = self.__jsonResponseResolve(ret)
			if ret.get('error'):
				return False
			
			return ret
		except Exception as e:
			print e

		return ret


	def __jsonResponseResolve(self, response):
		'''响应处理
		'''

		return json.loads(response)


	def run(self):
		'''程序入口
		'''
		with open('lasttime.json', 'r') as f:
			jstring = f.read()
			jstring = jstring.replace('\n', '')
			lasttime = json.loads(jstring)

			allList = self.getAllZhuanlanList()
			for zhuanlan in allList:
				zlid = zhuanlan.get('extra').get('column_id')
				title = zhuanlan.get('extra').get('column_title').encode('utf8')
				self.zhuanlan_dict[zlid] = title
				prev = lasttime.get(str(zlid)) or 0
				print zlid, prev
				prev = geek.getZhuanlan(zlid, prev, order = 'earliest')
				lasttime[str(zlid)] = prev
				# 跑完一个专栏存一次
				with open('lasttime.json', 'w') as ff:
					content = json.dumps(lasttime).replace('u', '')
					ff.write(content)

		return True


if __name__ == '__main__':
	geek = Geek(COOKIE, PROXY)
	geek.run()