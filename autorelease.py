# -*- coding:utf-8 -*-

import sys
import getopt
import os
from xml.etree import ElementTree as et
from subprocess import  Popen,PIPE

reload(sys)
sys.setdefaultencoding('utf-8')


def getFileList(path, fileList):
    assert isinstance(path, object)
    newDir = path
    if os.path.isfile(path):
        fileList.append(path.decode('utf-8'))
    elif os.path.isdir(path):
        for s in os.listdir(path):
            newDir = os.path.join(path, s)
            getFileList(newDir, fileList)
    return fileList


def usage():
    helpText = """
    -i input file
    -o out file
    -h print help info
    """
    print helpText


if '__main__' == __name__:
    project_path = ''
    input_file = ''
    out_file = ''

    if len(sys.argv) == 1:
        usage()
        sys.exit()

    opts, args = getopt.getopt(sys.argv[1:], "hp:", ["version", "file"])

    for op, value in opts:
        if op == '-p':
            # 获取输入的项目路径
            project_path = value
        elif op == '--version':
            print '1.0.0'
        else:
            usage()
            sys.exit()

    # 检查项目路径是否为空
    if project_path == '':
        print 'project path is Empty'
        sys.exit()

    # 项目路径是否存在
    if not os.path.exists(project_path):
        print '%s not exists' % (project_path)
        sys.exit()
    # 获取此路径下的所有文件
    if not os.path.isdir(project_path):
        project_path = os.path.join(project_path + os.sep + '.')
    project_name = ''
    for filename in os.listdir(project_path):
        if filename.find('xcworkspace') or filename.find('xcodeproj'):
            project_name = filename
    if project_name == '':
        print 'No Xcode project found'
        sys.exit()
    fileList = getFileList(project_path, [])

    # if not 'info.plist' in fileList:
    #     print 'not found info.plist file'
    #     sys.exit()
    infoPath = ''
    for filePath in fileList:
        if os.path.basename(filePath) == 'Info.plist':
            infoPath = filePath

    if infoPath == '':
        print 'not found info.plist file'
        sys.exit()

    root = et.parse(infoPath)
    if not root:
        print 'read info.plist fail'
        sys.exit()
    dicts = root.find('dict')

    findVersionKey = False
    mVersion = ''
    for node in dicts.getchildren():
        if node.text == 'CFBundleShortVersionString':
            findVersionKey = True
            continue
        if findVersionKey:
            version = node.text
            v = version.split('.')
            # 版本号+1
            v[-1] = str(int(v[-1]) + 1)
            seq = '.'
            node.text = seq.join(v)
            mVersion = node.text
            findVersionKey = False
            break
    if version == '' or mVersion == '':
        print 'from info.plist read version error'
        sys.exit()
    # 重新写入plist文件
    root.write(infoPath)
    print '当前版本：%s' % (mVersion)

    p = Popen(['xcrun','--help'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
    output = p.stdout.readlines()

    for out in output:
        print out
    errors = p.stderr.readlines()

    for e in errors:
        print e


    # print output
    # p.stdin.write(output)
    # os.system('xcrun' + "> /dev/null 2>&1")


