#-*- coding: utf-8 -*-
import sys
import codecs
import shelve

from aiml.LangSupport import mergeChineseSpace

def save(rule, temp):
	print temp
	template = """<aiml version="1.0.1" encoding="UTF-8">
	{rules}
	</aiml>
	"""

	category_template = """
		<category>
			<pattern>{pattern}</pattern>
			<template>
				{answer}
			</template>
		</category>"""
	db = shelve.open("simple_rules.db", "c", writeback=True)
	db[rule] = temp
	db.sync()
	rules = []
	for r in db:
		rules.append(category_template.format(pattern=r, answer=db[r]))
	content = template.format(rules="\n".join(rules))
	with open("auto-gen.aiml", "w") as fp:
		fp.write(content)

def learnFromUser(rule, temp):
	rule = mergeChineseSpace(unicode(rule, 'utf8')).encode("utf8")
	temp = mergeChineseSpace(unicode(temp, 'utf8')).encode("utf8")
	save(rule, temp)
	
import requests
import urllib
def learnFromSimsim(rule):
	#below, I will get temp from simsim
	temp = ""
	url = "http://www.simsimi.com/requestChat?lc=zh&ft=1.0&req=%s&uid=23528264"
	#print url % rule
	page = requests.get(url%rule)
	#print page.content
	temp = eval(page.content).get('res')
	#print temp
	save(rule, temp)
	#return res

	
if 3 == len(sys.argv):
	_, rule, temp = sys.argv
	learnFromUser(rule, temp)
elif 2 == len(sys.argv):
	_, rule = sys.argv
	learnFromSimsim(rule)

	
