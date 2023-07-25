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

# 是否下载 mp3，由于下载音频比较耗时，可以选择性下载
NEED_MP3 = False
```

# 下载我订阅的所有专栏列表
默认下载到当前目录的 download 目录下，以专栏名创建目录
```python
python geek.py
```

# 只下载某个专栏
```python
# 48是耗子叔的专栏 id《左耳听风》
python geek.py 48
```

# 生成 index.html索引页面
专栏下载完成后，为每个专栏生成一个 index 索引文件，方便在一个页面上查看