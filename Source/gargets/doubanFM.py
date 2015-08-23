#!/usr/bin/python
# coding:utf-8

import httplib
import json
import os
import sys
import subprocess
import time

reload(sys)
sys.setdefaultencoding("utf-8")
while True:
	#get song list
	httpConnection = httplib.HTTPConnection('douban.fm')
	httpConnection.request('GET','/j/mine/playlist?type=n&channel=4')
	song = json.loads(httpConnection.getresponse().read())['song']
	title = song[0]['albumtitle']
	picture = 'images/' + song[0]['picture'].split('/')[4]
	#play
	print 'start play: %s' % title
	player = subprocess.Popen(['mpg123',song[0]['url']])
	time.sleep(song[0]['length'])
	player.kill()
