#!/usr/bin/python
# coding:utf-8

import requests
import subprocess
from bs4 import BeautifulSoup
import time,os,sys

reload(sys)
sys.setdefaultencoding("utf-8")
while True:
	#get song list
	page = requests.get('http://www.scientificamerican.com/podcast/60-second-science/')
	soup = BeautifulSoup(page.content,"html.parser")
	songs = soup.find_all("audio", {"id":"podcastContentListPlayer"})
	songUrls = ["http://www.scientificamerican.com" + song['src'] for song in songs]
	#play
	for url in songUrls:
		print 'start play %s' % url
		player = subprocess.Popen(['mpg123', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		time.sleep(180)
		player.kill()
