#coding:utf8
import os

def genIndexHtml(rootDir, name):
    with open('%s/index.html' % rootDir, 'w') as index:
        index.write('<title>%s</title>' % name)
        index.write('<script>function alterTitle(title){document.title=title;}</script><style>.main{width:100%;height: 100%;} .side {float:left;max-width:200px;height:100%;overflow:scroll;border:1px solid;} .content {overflow:hidden;} </style>\n')
        index.write('<div class="main"><div class="side">')
        for root, dirs, files in os.walk(rootDir):
            files.sort()
            for f in files:
                if f.endswith('.html') and f != 'index.html':
                    index.write('<h6><a onclick="alterTitle(\'%s\')" target="main" href="%s">%s</a></h6>\n' % (f, f, f))

        index.write('</div><div class="content"><iframe width=100% height=100% name="main"/></div></div>')

def main():
    filters = ['.git', '.vscode', '.idea']
    for root, dirs, files in os.walk('./download'):
        for d in dirs:
            dir = os.path.join(root, d)
            flag = False
            for f in filters:
                if f in dir:
                    flag = True
                    break

            if flag:
                continue

            print dir
            genIndexHtml(os.path.join(root, d), d)

if __name__ == '__main__':
    main()