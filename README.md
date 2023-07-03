# geektime
将极客时间的专栏内容（文章和mp3）下载到本地方离线学习和笔记
需要登录态

```
仅供学习交流，请勿用于商业用途
```

# 登录态配置
在本地建一个 local.py文件，此文件只保存在本地，不会上传到 git，然后在local.py配置 cookie 和 proxy
```python
#coding:utf8

'''
访问代理等配置信息
'''

# 登录后的cookie，验证登录态
COOKIE = ''

# 访问代理设置
PROXY = {
    'http': '',
    'https': '',
}
```

# 下载我订阅的所有专栏列表
默认下载到当前目录的 download 目录下，以专栏名创建目录
```python
from geek import Geek

geek = Geek(cookie='', proxy='')
geek.run()
```

# 只下载某个专栏
```python
from geek import Geek

geek = Geek(cookie='', proxy='')
geek.getZhuanlan(116, 0, order = 'earliest')
```

# 生成 index.html索引页面
专栏下载完成后，为每个专栏生成一个 index 索引文件，方便在一个页面上查看
```
python genIndexHtml.py  
```