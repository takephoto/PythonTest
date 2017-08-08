# -*- coding: UTF-8 -*-

import urllib
import urllib2
from xml.etree import ElementTree as et
from model import User

def http_get(url,data):
    url_values = urllib.urlencode(data)
    request = urllib2.Request('%s%s%s' % (url, '?', url_values))
    response = urllib2.urlopen(request)
    return response

class ClinetAPI:
    def user_login(self,account,password):
        data = {}
        data['u'] = account
        data['p'] = password
        url = 'http://u.160.com/API/login.ashx'

        response = http_get(url, data)
        xml = response.read()
        doc = et.fromstring(xml)
        flag = doc.find('flag')

        if int(flag.text) == 1:
            user = User()
            user.id = int(doc.find('id').text)
            user.name = doc.find('name').text
            user.mail = doc.find('mail').text
            user.sid = doc.find('sid').text
            return user
        else:
            print '登录失败'

