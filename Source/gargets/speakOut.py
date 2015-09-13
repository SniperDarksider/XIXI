#!/usr/bin/python
# coding:utf-8

import httplib

def getToken():
	oauthUrl = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=jC4FZ417W3L4eihvthCTONSx&client_secret=b7cf572d7e1ec457b3948532159dc9bb"
	httpConnection = httplib.HTTPConnection("openapi.baidu.com")
	httpConnection.request('POST','/oauth/2.0/token?grant_type=client_credentials&client_id=jC4FZ417W3L4eihvthCTONSx&client_secret=b7cf572d7e1ec457b3948532159dc9bb')
	contents = eval(httpConnection.getresponse().read())
	#print type(contents)
	token = contents[u'access_token']
	return token

import os, sys
import subprocess
reload(sys)
sys.setdefaultencoding("utf-8")
def say(text, token):
	#per: 1 - male; 0 - female
	#pit: pitch
	#spd: speed, range - 1~9
	url = "http://tsn.baidu.com/text2audio?tex=%s&lan=zh&per=0&pit=3&spd=7&cuid=***&ctp=1&tok=%s" % (text, token)
	print url
	#os.system('mpg123 "%s"' % (url))
	player = subprocess.Popen(['mpg123', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
if '__main__' == __name__:
	#words = ["小懒猪快起床背单词啦",]
	token = getToken()
	say(sys.argv[1], token)