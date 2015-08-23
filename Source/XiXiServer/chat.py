#!/usr/bin/python
# coding:utf-8

import socket
import threading, time
import jieba

def get_id_address(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	ip = "0.0.0.0"
	try:
		ip = socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15]))[20:24])
	except:
		pass
	#global logger
	#logger.info("%s : %s" % (ifname,ip))
	return ip

def analyze(content,mode=True):
	seg_list = jieba.cut(content, cut_all=mode)
	return seg_list#"/".join(seg_list)
	
def getAnswer(words):
	return "/".join(words)

def chat(sock, addr):
	print "My darling is in %s:%s" % addr
	sock.send("I miss you so much, dariling (* ?3)(?? *)\n")
	while True:
		req = sock.recv(1024)
		print "you say: %s" % req
		#time.sleep(1)
		if "exit" == req or not req:
			sock.send('See you later. ( ^_^ )/~~)')
			print 'See you later. ( ^_^ )/~~)'
			break
		back = analyze(req)
		answer = getAnswer(back) + "\n"
		#print type(answer.encode('utf-8'))
		print "I think is as %s" % answer
		sock.send(answer.encode('utf-8'))
	sock.close()

	
IP = "127.0.0.1"
port = 13333

if "__main__" == __name__:
	IP = get_id_address("eth0")
	if "0.0.0.0" == IP:
		IP = get_id_address("wlan0")
	IP = "192.168.1.103"
	print "My address is %s:%s" % (IP, port)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((IP,port))
	s.listen(5)
	print "waiting for my darling..."
	while True:
		sock, addr = s.accept()
		t = threading.Thread(target=chat, args=(sock, addr))
		t.start()
	