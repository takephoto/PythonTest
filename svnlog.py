# -*- coding:utf-8 -*-

# 获取SVN上的日志信息

from subprocess import Popen, PIPE
import os
import sys
import Foundation

reload(sys)
sys.setdefaultencoding('utf-8')

class SvnLog:
    def __init__(self):
        self.worksapcePath = ''

    def getSvnLog(self):
        # type: () -> object
        curdir = os.curdir
        os.chdir(self.worksapcePath)
        p = Popen(['svn', 'log','-l','4000'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
        outs = p.stdout.readlines()
        errors = p.stderr.readlines()
        for e in errors:
            print e
        os.chdir(curdir)
        return outs

    # 过滤当前时间一周前的
    # 过滤当前时间15天前的
    # 过滤当前时间30天前的

    def filterlog(self, loglines):
        lines = []
        for l in loglines:
            # 过滤出指定日期的日志
            if l == '':
                lines.append(l)
        return lines


if __name__ == '__main__':
    svnlog = SvnLog()
    svnlog.worksapcePath = '/Users/admin/20170727/LifeCalendar'
    lines = svnlog.getSvnLog()
    infos = []

    start = False

    text = []
    headMap = {}
    allLogs = []

    for l in lines:
        # 开始标记
        if l[0] == '-' and not start:
            start = True
            headMap = {}
            text = []
            continue
        if l[0] == '-' and start:
            start = False
            headMap['text'] = text
            allLogs.append(headMap)
            continue
        # 提交记录信息
        if l[0] == 'r' and start:
            head = l.split('|')
            # 版本号
            ver = head[0]
            # 作者
            author = head[1]
            # 提交日期
            date = head[2]
            headMap = {
                'ver' : ver ,
                'author' : author,
                'date' : date
            }
            continue
        if l == '\n' and start:
            continue
        text.append(l)

    count = {}
    print 'svn总提交次数：%d' % len(allLogs)
    for dict in allLogs:
        name = dict['author']
        if count.has_key(name):
            v = count[name] + 1
        else:
            v = 1
        count[name] = v
    print count