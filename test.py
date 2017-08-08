import urllib2
import urllib
import base64
import os
import md5
import requests
import re
from bs4 import BeautifulSoup

baseURL = "http://sz.58.com/chuzu/?PGTID=0d100000-0000-4596-b469-cddad143a70b&ClickID=1"
response = urllib2.urlopen(baseURL)
html = response.read()

soup = BeautifulSoup(html,"lxml")
#print soup.prettify()
print soup.title
print soup.head
print soup.a
print soup.p
print soup.p.name
print soup.p.attrs
print soup.p['class']
print soup.p.get('class')
soup.p['class'] = 'head'

print soup.p

del soup.p['class']
print soup.p
print soup.p.string
print soup.head.contents[1]

for children in soup.head.children:
    print children

for children in soup.head.descendants:
    print children.string

f = open('Url.txt')
f.write('name is text')








