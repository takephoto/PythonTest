# -*- coding:utf-8 -*-

import sys
import getopt
import os
from xml.etree import ElementTree as et
from subprocess import Popen,PIPE
import datetime
import shutil



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

    #检查项目路径是否为空
    if project_path == '':
        print 'project path is Empty'
        sys.exit()

    # 项目路径是否存在
    if not os.path.exists(project_path):
        print '%s not exists' % (project_path)
        sys.exit()

    if not os.path.isdir(project_path):
        project_path = os.path.join(project_path + os.sep + '.')
    project_name = ''
    # 遍历此路径下的所有文件，找到后缀为xcworkspace xcodeproj文件
    for f in os.listdir(project_path):
        # pod 项目
        if not f.find('xcworkspace') == -1:
            project_name = f
        # xcode 项目
        if not f.find('xcodeproj') == -1:
            project_name = f

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
            break

    if infoPath == '':
        print 'not found info.plist file'
        sys.exit()

    print infoPath
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


    # 重定向输入输出

    archiveFile = project_name.split('.')[0] + '.' + 'xcarchive'
    archiveFullPath = os.curdir + os.sep + 'xcarchive' + os.sep + archiveFile
    sdk = 'iphoneos'
    scheme = project_name.split('.')[0]
    configuration = 'Release'
    if not project_path[-1] == os.sep:
        workspace = project_path + os.sep + project_name
    else:
        workspace = project_path + project_name
    print '==>' + workspace

    if os.path.exists(archiveFullPath):
        shutil.rmtree(archiveFullPath)

    curdir = os.curdir
    if project_name.split('.')[-1] == 'xcodeproj':
        os.chdir(project_path)
        if os.path.exists(archiveFullPath):
            shutil.rmtree(archiveFullPath)
        cmdList = ['xcodebuild', '-archivePath', archiveFullPath, '-sdk', sdk, '-scheme',
               scheme, '-configuration', configuration, 'archive']
    else:
        cmdList = ['xcodebuild', '-archivePath', archiveFullPath, '-workspace', workspace, '-sdk', sdk, '-scheme',
               scheme, '-configuration', configuration, 'archive']

    # 删除之前打包好的归档文件
    # if os.path.exists(archiveFullPath) and os.path.i:
    #     os.removedirs(archiveFullPath)

    cmd = 'xcodebuild -archivePath %s -workspace %s -sdk %s -scheme %s -configuration %s archive' % (archiveFullPath, workspace, sdk, scheme, configuration)
    print cmd
    p = Popen(cmdList, stdout=PIPE, stderr=PIPE, stdin=PIPE)

    output = p.stdout.readlines()
    for out in output:
        if not out.find('ARCHIVE FAILED') == -1:
            print 'ARCHIVE FAILED'
            sys.exit()
        print out

    errors = p.stderr.readlines()

    for e in errors:
        print e

    os.chdir(curdir)

    # 导出IPA 文件
    # ipa 文件路径

    ipafileName = project_name.split('.')[0] + '.ipa'
    exportIPAPath = os.curdir + os.sep + 'ipa' + os.sep + ipafileName
    exportCmdList = ['xcodebuild', '-exportArchive', '-archivePath', archiveFullPath, '-exportPath', exportIPAPath, '-exportOptionsPlist','options.plist']
    print exportCmdList
    p = Popen(exportCmdList, stdout=PIPE, stderr=PIPE, stdin=PIPE)

    output = p.stdout.readlines()
    for out in output:
        # if not out.find('ARCHIVE FAILED') == -1:
        #     print 'ARCHIVE FAILED'
        #     sys.exit()
        print out
    errors = p.stderr.readlines()
    for e in errors:
        print e



