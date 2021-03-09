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


ZHUAN_DICT = {
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
            116: '深入剖析Kubernetes',
        }
        
try:
    from local import *
except:
    pass