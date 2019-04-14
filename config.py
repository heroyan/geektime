#coding:utf8

'''
访问代理等配置信息
'''

# 登录后的cookie，验证登录态
COOKIE = ''

# 访问代理设置
PROXY = {
    'http or https': 'your webproxy domain and port'
}

try:
    from local import *
except:
    pass