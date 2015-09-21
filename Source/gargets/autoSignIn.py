#!/usr/bin/python
#-*- coding:utf-8 -*-
from __future__ import unicode_literals

import ConfigParser
import cookielib
import urllib2,urllib
import json
from bs4 import BeautifulSoup
import re
import logging

class Site(object):
	def __init__(self, sitename=""):
		self._cookie = cookielib.LWPCookieJar()
		self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cookie))
		self._logger = logging.getLogger(__name__)
		self._logger.setLevel(logging.INFO)
		self._handler = logging.FileHandler('gargets_autoSignIn.log')
		self._handler.setLevel(logging.INFO)
		self._handler.setFormatter(logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s'))
		self._logger.addHandler(self._handler)
		self._sitename = sitename

	def login(self, respParserFunc,method="GET",headers={}, data={"user":"","psw":""}):
		print "user is: ", user
		self._logger.info("begin to login in %s, user is: %s" % (sitename,user))
		req = urllib2.Request(self.LOGIN_URL, headers = headers)
		resp, result = "", ""
		if "GET" == method:
			resp = self._opener.open(req)
		else:
			resp = self._opener.open(req, urllib.urlencode(data).encode("utf-8"))
		result = respParserFunc(resp)
		print result
		self._logger.info(result)

	def signIn(self, method="GET"):
		pass


class Baidu(object):
	def __init__(self):
		self._cookie = cookielib.LWPCookieJar()
		self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cookie))
		self.INDEX_URL = "http://www.baidu.com"
		self.TOKEN_URL = "https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3"
		self.LOGIN_URL = "https://passport.baidu.com/v2/api/?login"
		self._logger = logging.getLogger(__name__)
		self._logger.setLevel(logging.INFO)
		self._handler = logging.FileHandler('gargets_autoSignIn.log')
		self._handler.setLevel(logging.INFO)
		self._handler.setFormatter(logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s'))
		self._logger.addHandler(self._handler)

	def login(self,user="",psw=""):
		print "user is: ", user
		self._logger.info("user is: %s" % user)
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
		if resp and resp["no"] == 0:
			print "Login Success!"
			self._logger.info("Login Success!")
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
				self._logger.info(u"%s %s" % (signData['kw'].decode("utf-8"), u"吧签到成功!!"))
			elif resp["no"] == 1101:
				print signData['kw'], "吧之前已经签到过了喔~".encode("utf-8")
				self._logger.info(u"%s %s" % (signData['kw'].decode("utf-8"),"吧之前已经签到过了喔~"))
			else:
				print "未知错误！\n".encode("utf-8"), url, "\n", resp
				self._logger.info(u"未知错误！\n %s \n %s" % ( url,resp))


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
			self._logger.info("百度知道签到成功~")
		elif resp["errno"] == 2:
			print "百度知道之前已经签到过了喔~".encode("utf-8")
			self._logger.info("百度知道之前已经签到过了喔~")
		else:
			print "未知错误！\n".encode("utf-8"), resp
			self._logger.info("未知错误！\n %s" % resp)
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
			self._logger.info("抽奖获得：%s" % resp["data"]["prizeList"][0].get("goodsName"))
		else:
			print "未知错误！\n".encode("utf-8"), resp
			self._logger.info("未知错误！\n %s" % resp)

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

import hashlib
import random,time
#bulo.hujiang.com
class Hujiang(object):
	def __init__(self):
		self._cookie = cookielib.LWPCookieJar()
		self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cookie))
		self.INDEX_URL = "http://bulo.hujiang.com/"
		self._callback = "jQuery18307142652559559792_1442495521490"
		# now we know that the parameter "_" is the timestamp according to jsonp
		### but I still don't know how to get the value of parameter callback, it seems that the value of "callback" is irrelative
		self.TOKEN_URL = "http://pass.hujiang.com/quick/account/?callback=%s&account=%s&password=%s&code=&act=loginverify&source=bulo_anon&_=%s"
		self.LOGIN_URL = "http://pass.hujiang.com/quick/synclogin.aspx?token=%s&remeberdays=14&callback=%s&_=%s"
		self._logger = logging.getLogger(__name__)
		self._logger.setLevel(logging.INFO)
		self._handler = logging.FileHandler('gargets_autoSignIn.log')
		self._handler.setLevel(logging.INFO)
		self._handler.setFormatter(logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s'))
		self._logger.addHandler(self._handler)

	def login(self,user="",psw=""):
		print "user is: ", user
		self._logger.info("user is: %s" % user)
		self._getToken(user,psw)
		hjHeaders = {
                "Accept":"*/*",
                "Accept-Encoding":"gzip, deflate, sdch",
                "Accept-Language":"zh-CN,zh;q=0.8",
                "Host":"pass.hujiang.com",
                "Referer":"http://bulo.hujiang.com/anon/?source=nbulo&returnurl=http%3a%2f%2fbulo.hujiang.com%2fhome%2f",
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
             }
		#print self.LOGIN_URL%(user,self._md5(psw))
		req = urllib2.Request(self.LOGIN_URL%(self._token,self._callback,str(int(time.time()*1000))), headers = hjHeaders)
		resp = eval(self._opener.open(req).read().decode("utf-8").replace(self._callback,"").replace(";",""))
		if resp["code"] == 0:
			print "Login Success!"
			self._logger.info("Login Success!")
			return self._opener
		else:
			print "Wooooo, there must be something wrong~", resp["code"].encode("utf-8"), resp["message"].encode("utf-8")
			self._logger.info("Wooooo, there must be something wrong~\n code = %s \n message = %s \n" % (resp["code"].encode("utf-8"), resp["message"].encode("utf-8")))

	def _md5(self,pwd):
		m = hashlib.md5()
		m.update(pwd)
		return m.hexdigest()
	def _getToken(self,user,psw):
		hjHeaders = {
                "Accept":"*/*",
                "Accept-Encoding":"gzip, deflate, sdch",
                "Accept-Language":"zh-CN,zh;q=0.8",
                "Host":"pass.hujiang.com",
                "Referer":"http://bulo.hujiang.com/anon/?source=nbulo&returnurl=http%3a%2f%2fbulo.hujiang.com%2fhome%2f",
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
             }
		req = urllib2.Request(self.TOKEN_URL%(self._callback,user,self._md5(psw),str(int(time.time()*1000))), headers = hjHeaders)
		true, false, null = 'true', 'false', ''
		resp = eval(self._opener.open(req).read().replace(self._callback,""))
		#print resp
		if resp["code"] == 0:
			print "Get Token succeed~~"
			self._logger.info("Get Token succeed~~")
			self._token = resp["data"]["ssotoken"]
		else:
			print "Wooooo, there must be something wrong~", resp[code], resp[message]
			self._logger.info("Wooooo, there must be something wrong~\n code = %s \n message = %s \n" % (resp["code"].encode("utf-8"), resp["message"].encode("utf-8")))

	#签到
	def signIn(self):
		signHeaders = {
				"Accept":"application/json, text/javascript, */*; q=0.01",
				"Accept-Encoding":"gzip, deflate, sdch",
				"Accept-Language":"zh-CN,zh;q=0.8",
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36 LBBROWSER",
                "Host":"bulo.hujiang.com",
                "Referer":"http://bulo.hujiang.com/home/",
              }
        #http://bulo.hujiang.com/app/api/ajax_take_card.ashx?0.492593998551094
		SIGN_URL = "http://bulo.hujiang.com/app/api/ajax_take_card.ashx?%.17f"
		req = urllib2.Request(SIGN_URL%random.random(), headers = signHeaders)
		resp = self._opener.open(req).read()
		try:
			if int(resp[0]) > 0:
				print "打卡成功，获得%s沪元，共打卡%s天~~" % (resp[0],resp[1])
				self._logger.info(u"打卡成功，获得%s沪元，共打卡%s天~~" % (resp[0],resp[1]))
			if int(resp[0]) == 0:
				print "已经打过卡了喔~~"
				self._logger.info(u"已经打过卡了喔~~")
			if int(resp[0]) == -1:
				print "用户未激活"
				self._logger.info(u"用户未激活")
		except Exception, e:
			print resp
			self._logger.info(u"未知错误！\n %s" % resp)

#http://www.mafengwo.cn/
class Mafengwo(object):
	def __init__(self):
		self._cookie = cookielib.LWPCookieJar()
		self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cookie))
		self.LOGIN_URL = "https://passport.mafengwo.cn/login-popup.html"
		self._logger = logging.getLogger(__name__)
		self._logger.setLevel(logging.INFO)
		self._handler = logging.FileHandler('gargets_autoSignIn.log')
		self._handler.setLevel(logging.INFO)
		self._handler.setFormatter(logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s'))
		self._logger.addHandler(self._handler)

	def login(self,user="",psw=""):
		print "user is: ", user
		self._logger.info("user is: %s" % user)
		mfwHeaders = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding":"gzip, deflate",
                "Accept-Language":"zh-CN,zh;q=0.8",
                "Origin":"https://passport.mafengwo.cn",
                "Host":"passport.mafengwo.cn",
                "Referer":"https://passport.mafengwo.cn/login-popup.html",
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
             }

		bdData = {
			"passport":user,
			"password":psw,
			"code":"",
		}
		req = urllib2.Request(self.LOGIN_URL, headers = mfwHeaders)
		resp = self._opener.open(req, urllib.urlencode(bdData).encode("utf-8"))
		if 200 == resp.getcode():
			print "Login Success!"
			self._logger.info("Login Success!")
		elif 302 == resp.getcode():
			resp = self._opener.open(req)
			if 200 == resp.getcode():
				print "Login Success!"
				self._logger.info("Login Success!")
			else:
				print "Wooooo, there must be something wrong~"
				self._logger.info("Wooooo, there must be something wrong~")
		else:
			print "Wooooo, there must be something wrong~"
			self._logger.info("Wooooo, there must be something wrong~")

	#签到
	def signIn(self):
		signHeaders = {
				"Accept":"text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
				"Accept-Encoding":"gzip, deflate",
				"Accept-Language":"zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3",
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36 LBBROWSER",
                "Host":"www.mafengwo.cn",
                "Referer":"http://www.mafengwo.cn/",
              }
        #http://www.mafengwo.cn/ajax/ajax_japp.php?callback=jQuery18105755553864366139_1442836474475&app=daka&loaded_modules=%2Fjs%2FDropdown%2CInputListener%2CSuggestionXHR%2CDropList%2CSuggestion%2C%2Fjs%2FSiteSearch%2Cjq-upnum%2Cdialog%2FLayer%2Cdialog%2FDialogBase%2Cdialog%2FDialog%2CTopTip%2CSlider%2Cjq-mousewheel%2CScrollBar%2CCookie%2Cxdate%2Cjqui-core%2Cjqui-datepicker%2CDateRangePicker%2Cjq-tmpl%2CPagination%2CStorage%2Cjq-jgrowl&params=%7B%7D&_=1442836608590
		ts = int(time.time()*1000)
		SIGN_URL = "http://www.mafengwo.cn/ajax/ajax_japp.php?callback=jQuery18105755553864366139_%s&app=daka&loaded_modules=%%2Fjs%%2FDropdown%%2CInputListener%%2CSuggestionXHR%%2CDropList%%2CSuggestion%%2C%%2Fjs%%2FSiteSearch%%2Cjq-upnum%%2Cdialog%%2FLayer%%2Cdialog%%2FDialogBase%%2Cdialog%%2FDialog%%2CTopTip%%2CSlider%%2Cjq-mousewheel%%2CScrollBar%%2CCookie%%2Cxdate%%2Cjqui-core%%2Cjqui-datepicker%%2CDateRangePicker%%2Cjq-tmpl%%2CPagination%%2CStorage%%2Cjq-jgrowl&params=%%7B%%7D&_=%s" % (str(ts), str(ts+33))
		print SIGN_URL
		req = urllib2.Request(SIGN_URL, headers = signHeaders)
		resp = self._opener.open(req).read()
		print repr(resp)
		resp = eval(resp.replace("jQuery18105755553864366139_"+str(ts),""))
		if len(resp["css"]) != 0:
			print "打卡成功~~"
			self._logger.info("打卡成功~~")
		else:
			print resp
			self._logger.info(u"未知错误！\n %s" % resp.encode("utf-8",errors="ignore"))

if "__main__" == __name__:
	#read configuration file
	configFile = "user_config.ini"
	cf = ConfigParser.ConfigParser()
	cf.read(configFile)
	#mafengwo auto sign in
	#username = cf.get("mafengwo", "username")
	#pwd = cf.get("mafengwo","password")
	#mfw = Mafengwo()
	#mfw.login(username,pwd)
	#mfw.signIn()
	#hujiang atuo sign in
	username = cf.get("hujiang","username")
	pwd = cf.get("hujiang","password")
	hj = Hujiang()
	hj.login(username,pwd)
	hj.signIn()
	username = cf.get("baidu","username")
	pwd = cf.get("baidu","password")
	#baidu auto sign in
	bd = Baidu()
	bd.login(username,pwd)
	bd.tiebaSignIn()
	bd.zhidaoSignIn()

