#!/usr/bin/python
#-*- coding:utf-8 -*-
from __future__ import unicode_literals

import ConfigParser
import cookielib
import urllib2,urllib
import json
from bs4 import BeautifulSoup
import re
class Baidu(object):
	def __init__(self):
		self._cookie = cookielib.LWPCookieJar()
		self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cookie))
		self.INDEX_URL = "http://www.baidu.com"
		self.TOKEN_URL = "https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3"
		self.LOGIN_URL = "https://passport.baidu.com/v2/api/?login"

	def login(self,user="",psw=""):
		print "user is: ", user
		self._initial()
		self._getToken()
		bdHeaders = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding":"gzip,deflate,sdch",
                "Accept-Language":"en-US,en;q=0.8,zh;q=0.6",
                "Host":"passport.baidu.com",
                "Origin":"http://www.baidu.com",
                "Referer":"http://www.baidu.com/",
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
             }
		bdData = {
			"staticpage":"https://www.baidu.com/cache/user/html/v3Jump.html",
			"token":self._token,
			"tpl":"mn",
			"username":user,
			"password":psw,
		}
		req = urllib2.Request(self.LOGIN_URL, headers = bdHeaders)
		resp = self._opener.open(req, urllib.urlencode(bdData).encode("utf-8"))
		resp = json.loads(self._opener.open("http://tieba.baidu.com/f/user/json_userinfo").read().decode("utf-8"))
		if resp["no"] == 0:
			print "Login Success!"
			return self._opener
		else:
			print "Wooooo, there must be something wrong~"

	def _getToken(self):
		self._token = eval(self._opener.open(self.TOKEN_URL).read())['data']['token']
		#print self._token

	def _initial(self):
		self._opener.open(self.INDEX_URL)

	#百度贴吧签到
	def _getMyTiebaURL(self):
		LIKETIEBA_URL = "http://tieba.baidu.com/f/like/mylike"
		page = self._opener.open(LIKETIEBA_URL).read().decode("gbk")
		soup = BeautifulSoup(page,"html.parser")
		trs = soup.find_all("tr")
		MAIN_URL = "http://tieba.baidu.com/"
		return [tr.contents[0].a["title"] + "::" + MAIN_URL + tr.contents[0].a["href"] for tr in trs[1:]]
	def getTbTbs(self, url):
		reg_getTbs = re.compile("PageData.tbs = \"(\w+)\"|\'tbs\': \"(\w+)|\'tbs\':\'(\w+)")
		return reg_getTbs.findall(self._opener.open(url).read().decode("UTF-8"))[0]
	def tiebaSignIn(self):
		likeUrls = self._getMyTiebaURL()
		#print likeUrls
		signHeaders = {
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36 LBBROWSER",
                "Host":"tieba.baidu.com",
                "Origin":"http://tieba.baidu.com",
                "Referer":"http://tieba.baidu.com",
              }
		signData = {
			"ie":"utf-8",
			"kw":"",
			"tbs":"",
		}
		SIGN_URL = "http://tieba.baidu.com/sign/add"
		for item in likeUrls:
			title, url = item.split("::")
			signData['kw'] = title.encode("utf-8")
			signData["tbs"] = self.getTbTbs(url)
			signHeaders["Referer"] = url
			req = urllib2.Request(SIGN_URL, headers = signHeaders)
			#print type(signData)
			resp = json.loads(self._opener.open(req, urllib.urlencode(signData).encode("utf-8")).read().decode("utf-8"))
			if resp["no"] == 0:
				print signData['kw'], u"吧签到成功!!".encode("utf-8")
			elif resp["no"] == 1101:
				print signData['kw'], "吧之前已经签到过了喔~".encode("utf-8")
			else:
				print "未知错误！\n".encode("utf-8"), url, "\n", resp


	#百度知道签到：fail
	def zhidaoSignIn(self):
		signHeaders = {
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36",
			"Host":"zhidao.baidu.com",
			"Origin":"http://zhidao.baidu.com",
			"Referer":"http://zhidao.baidu.com/",
		}
		signData = {
			"cm":"100509",
			"utdata":"95,95,103,101,101,111,101,98,95,103,98,98,102,122,111,102,102,14416306630860",
			"stoken":"515059124497113e93126446a1d4e144"}
		SIGN_URL = "http://zhidao.baidu.com/submit/user"
		#SIGN_URL = "http://zhidao.baidu.com/ihome/api/signInfo?t=1441461853468"
		req = urllib2.Request(SIGN_URL, headers = signHeaders)
		resp = json.loads(self._opener.open(req).read().decode("utf-8"))
		if resp["errorNo"] == 0:
			print "百度知道签到成功~".encode("utf-8")
		elif resp["errno"] == 2:
			print "百度知道之前已经签到过了喔~".encode("utf-8")
		else:
			print "未知错误！\n".encode("utf-8"), resp
	#百度知道抽奖
	def zhidaoLottery(self):
		lotteryHeaders = {
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36",
			"Host":"zhidao.baidu.com",
			#"Origin":"http://zhidao.baidu.com",
			"Referer":"http://zhidao.baidu.com/shop/lottery",
		}
		lotteryData = {}
		LOTTERY_URL = "http://zhidao.baidu.com/shop/submit/lottery?type=0&token=%s&_=%s"
		#SIGN_URL = "http://zhidao.baidu.com/ihome/api/signInfo?t=1441461853468"
		req = urllib2.Request(LOTTERY_URL, headers = signHeaders)
		resp = json.loads(self._opener.open(req).read().decode("utf-8"))
		if resp["errno"] == 0:
			print "抽奖获得：".encode("utf-8"), resp["data"]["prizeList"][0].get("goodsName")
		else:
			print "未知错误！\n".encode("utf-8"), resp

#www.readcolor.com
class readfar(object):
	def __init__(self):
		self._cookie = cookielib.LWPCookieJar()
		self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cookie))
		self.INDEX_URL = "http://readcolor.com/"
		self.TOKEN_URL = "https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3"
		self.LOGIN_URL = "https://passport.baidu.com/v2/api/?login"

	def login(self,user="",psw=""):
		print "user is: ", user
		self._initial()
		self._getToken()
		bdHeaders = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding":"gzip,deflate,sdch",
                "Accept-Language":"en-US,en;q=0.8,zh;q=0.6",
                "Host":"passport.baidu.com",
                "Origin":"http://www.baidu.com",
                "Referer":"http://www.baidu.com/",
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
             }
		bdData = {
			"staticpage":"https://www.baidu.com/cache/user/html/v3Jump.html",
			"token":self._token,
			"tpl":"mn",
			"username":user,
			"password":psw,
		}
		req = urllib2.Request(self.LOGIN_URL, headers = bdHeaders)
		resp = self._opener.open(req, urllib.urlencode(bdData).encode("utf-8"))
		resp = json.loads(self._opener.open("http://tieba.baidu.com/f/user/json_userinfo").read().decode("utf-8"))
		if resp["no"] == 0:
			print "Login Success!"
			return self._opener
		else:
			print "Wooooo, there must be something wrong~"

	def _getToken(self):
		self._token = eval(self._opener.open(self.TOKEN_URL).read())['data']['token']
		#print self._token

	def _initial(self):
		self._opener.open(self.INDEX_URL)

	#签到
	def signIn(self):
		signHeaders = {
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36 LBBROWSER",
                "Host":"readcolor.com",
                "Referer":"http://readcolor.com/",
              }
		SIGN_URL = "http://readcolor.com/users/sign"
		req = urllib2.Request(SIGN_URL, headers = signHeaders)
		resp = json.loads(self._opener.open(req).read().decode("utf-8"))
		if resp["succeed"] == "true":
			print "签到成功!!"
		elif resp["succeed"] == "false":
			print "之前已经签到过了喔~"
		else:
			print "未知错误！\n", resp

if "__main__" == __name__:
	#read configuration file
	configFile = "user_config.ini"
	cf = ConfigParser.ConfigParser()
	cf.read(configFile)
	username = cf.get("baidu","username")
	pwd = cf.get("baidu","password")
	#baidu auto sign in
	bd = Baidu()
	bd.login(username,pwd)
	bd.tiebaSignIn()
	bd.zhidaoSignIn()

