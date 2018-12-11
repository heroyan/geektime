#coding:utf8
import urllib, urllib2
import json
import os
import time

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
			'getArticleContent': 'https://time.geekbang.org/serv/v1/article'
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
			139: '左耳听MySQL实战45讲',
		}


	def getArticles(self, cid, timestamp, limit, order = 'newest'):
		''' 得到专栏的列表
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
		'''
		art = self.getArticleContent(article_id)
		audio_download_url = art.get('audio_download_url')
		article_content = art.get('article_content')
		article_title = art.get('article_title')

		print article_title

		self.saveContent(zhuanlanid, '%s.html' % article_title, article_content)

		if audio_download_url:
			audio = self.getStaticResouce(audio_download_url)
			geek.saveContent(zhuanlanid, '%s.mp3' % article_title, audio)


	def getZhuanlan(self, zhuanlanid, timestamp, limit = 20, order = 'newest'):
		'''处理一个专栏
		@param zhuanlanid 
		@param timestamp 分页拉取的上批次文章的最大或最小文章时间戳
		@param limit 分页的页大小
		@param order 排序方式 newest文章从新到旧，earliest则相反
		'''
		while True:
			article_list = self.getArticles(zhuanlanid, timestamp, limit, order)
			if not article_list or (timestamp > 0 and article_list[0].get('score') > timestamp):
				break

			if timestamp > 0 and order == 'newest' and article_list[0].get('score') > timestamp:
				break

			if timestamp > 0 and order == 'earliest' and article_list[0].get('score') < timestamp:
				break

			for article in article_list:
				timestamp = article.get('score')
				article_id = article.get('id')

				print 'article_id', article_id, 'timestamp', timestamp

				self.getAndSaveArticle(zhuanlanid, article_id)

				# 限制时间，不要太频繁请求人家的服务器啦，做人要厚道
				time.sleep(1)


	def saveContent(self, zhuanlanid, file_name, content):
		'''保存内容到本地
		'''
		current_dir_path = os.path.dirname(os.path.realpath(__file__))
		zhuanlanpath = os.path.join(current_dir_path, self.zhuanlan_dict.get(zhuanlanid))
		if not os.path.exists(zhuanlanpath):
			os.mkdir(zhuanlanpath)

		file_path = os.path.join(zhuanlanpath, file_name.encode('utf8').replace('/', '-'))
		with open(file_path, 'wb') as f:
			try:
				f.write(content.encode('utf8'))
			except Exception as e:
				f.write(content)
			

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


if __name__ == '__main__':
	cookie = ''
	geek = Geek(cookie, {'http': 'web-proxy.tencent.com:8080'})
	#geek.getZhuanlan(81, 1527721200000)
	#geek.getZhuanlan(63, 1514109600000)
	#geek.getZhuanlan(113, 1535990400000)
	# =====to get
	# geek.getZhuanlan(140, 1544371200352, order = 'earliest')
	# geek.getZhuanlan(143, 1544371200646, order = 'earliest')
	# geek.getZhuanlan(126, 1544371200199, order = 'earliest')
	# geek.getZhuanlan(79, 1544137200503, order = 'earliest')
	# 花花的账号
	geek.getZhuanlan(80, 0, order = 'earliest')
	geek.getZhuanlan(139, 0, order = 'earliest')
