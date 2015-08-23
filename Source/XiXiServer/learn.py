import sys
import codecs
import shelve

from aiml.LangSupport import mergeChineseSpace

db = shelve.open("simple_rules.db", "c", writeback=True)

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
	
if 3 == len(sys.argv):
	_, rule, temp = sys.argv
	rule = mergeChineseSpace(unicode(rule, 'utf8')).encode("utf8")
	temp = mergeChineseSpace(unicode(temp, 'utf8')).encode("utf8")
	db[rule] = temp
	db.sync()
	rules = []
	for r in db:
		rules.append(category_template.format(pattern=r, answer=db[r]))
	content = template.format(rules="\n".join(rules))
	with open("auto-gen.aiml", "w") as fp:
		fp.write(content)
