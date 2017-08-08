# -*- coding: UTF-8 -*-

import socket
from clientAPI import ClinetAPI
import struct
import json.tool


# client = socket.socket()
# client.connect(('127.0.0.1',8080))
# len = client.send('你好的你哦')
#
# if len > 0 :
#     print '发送成功'
# else:
#     print '发送失败'

address = ('service.rili.updrv.com',2301)
def getSession(uid,sid):
    c = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    data = '1'
    fmt = 'cc4c2c'
    #bin_buff = struct.pack(fmt, 0x3C, 0, uid, sid)
    # data = str('0000000000000') + str(0x3C) + str(0) + str(uid) + sid
    # byte_buff = bytes(data)
    byte_buff = bytearray()
    byte_buff[0:12] = bytes('0000000000000')
    print len(byte_buff)
    byte_buff[12:13] = bytes(0x3C)
    print len(byte_buff)
    byte_buff[13:14] = bytes(0)
    print len(byte_buff)

    byte_buff[14:4] = bytes(uid)
    print len(byte_buff)
    print sid
    byte_buff[18:2] = bytes(str(len(sid)))
    byte_buff[20:2] = bytes(sid)
    print len(byte_buff)
    print str(byte_buff)
    print len(byte_buff)
    #
    # ba = bytearray()
    # print type(ba)
    # ba[0:1] = 0x3C
    # ba[1:2] = 0
    # ba[2:6] = uid
    # ba[8:12] = sid

    # str_buff = struct.unpack(fmt,bin_buff)
    print  len(data)
    length = c.sendto(str(byte_buff),address)
    data, addr = c.recvfrom(2048)
    if not data:
        c.close()
        print '获取会话失败'
        return
    else:
        print 'recv', data, 'from', addr

# 登录账号
client = ClinetAPI()
user = client.user_login("wx6666", "666666")

if user.sid and user.id:
    # 获取会话id
    getSession(user.id, user.sid)
name = ('name', 10, 78, 0x01)
print type(name)






