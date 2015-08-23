#!/usr/bin/python
# coding:utf-8

import requests
from bs4 import BeautifulSoup
import time,os,sys
from speakOut import *

#读书发声
def read(title, text):
	token = getToken()
	print title
	if title:
		say(title,token)
		time.sleep(3)
	ps = text.split("\n")
	for p in ps:
		#print p
		if p:
			say(p,token)
			time.sleep(1)

#简书(www.jianshu.com)第一篇
def jianshu():
	home = "http://www.jianshu.com"
	page = requests.get(home)
	soup = BeautifulSoup(page.content,"html.parser")
	titles = soup.find_all("h4",{"class":"title"})
	if len(titles) > 0:
		url = home + titles[0].a["href"]
		print url
		print "=" * 20
		title = titles[0].text
		page = requests.get(url)
		soup = BeautifulSoup(page.content,"html.parser")
		contents = soup.find_all("div",{"class":"show-content"})
		#print contents
		if len(contents)>0:
			content = contents[0].text
			read(title,content)	

#每日一文(www.meiriyiwen.com)第一篇
def meiriyiwen():
	url = "http://www.meiriyiwen.com/"
	page = requests.get(url)
	soup = BeautifulSoup(page.content,"html.parser")
	titles = soup.find_all("div",{"id":"article_show"})
	if len(titles) > 0:
		#read("",titles[0].text.decode("utf-8"))
		print titles[0].text.decode("utf-16")

if 2 == len(sys.argv):
	_, blog = sys.argv
	if "jianshu" == blog:
		jianshu()
	if "meiriyiwen" == blog:
		meiriyiwen()