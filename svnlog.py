# -*- coding:utf-8 -*-

# 获取SVN上的日志信息

from subprocess import Popen, PIPE
import os

class SvnLog:
    def __init__(self):
        self.worksapcePath = ''

    def getSvnLog(self):
        # type: () -> object
        curdir = os.curdir
        os.chdir(self.worksapcePath)
        p = Popen(['svn', 'log'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
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
    lines = svnlog.getSvnLog()
    for l in lines:
        print l
