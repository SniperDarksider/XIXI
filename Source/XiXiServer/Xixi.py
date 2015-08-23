import aiml
import jieba

# 分词
def analyze(content,mode=True):
	seg_list = jieba.cut(content, cut_all=mode)
	return " ".join(seg_list)
	
#创建核心，并学习AIML文件
kernel = aiml.Kernel()
kernel.learn("xixi-startup.xml")
kernel.respond("load aiml b")

while True:
	#res = analyze(raw_input("You >> "))
	#print res
	ask = raw_input("You >> ")
	print kernel.respond(ask)
	if "exit" == ask:
		break
	