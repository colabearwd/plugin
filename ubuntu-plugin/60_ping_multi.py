#!/usr/bin/python
#coding=utf-8

#TODO-当修改了数据库，需要修改本文的args_ipversion

import commands
import time
import copy
import json
import requests
import re
from multiprocessing.dummy import Pool as ThreadPool

#把结果和一些tag组成字符串，添加到payload
def load_data(ping_dict,res):
    	loss_rate = res[0]
    	max_time = res[1]
    	average_time = res[2]
    	URL = ping_dict['args_url']
    	if ( ping_dict['args_ipversion'] == 0 ):
        	VERSION = 'ipv4'
    	else:
        	VERSION = 'ipv6'
    	getuname = "uname -n"
    	status ,UNAME = commands.getstatusoutput(getuname)
	ts = int(time.time())
	item1 = {"metric":"ping.loss_rate","endpoint":UNAME,"tags":"target="+URL+",ip-version="+VERSION,"value":loss_rate,"timestamp":ts,"counterType":"GAUGE","step":60}
	item2 = {"metric": "ping.max_time","endpoint": UNAME,"tags": "target="+URL+",ip-version="+VERSION,"value": max_time,"timestamp": ts,"counterType": "GAUGE","step": 60}
	item3 = {"metric": "ping.average_time","endpoint": UNAME,"tags": "target="+URL+",ip-version="+VERSION,"value": average_time,"timestamp": ts,"counterType": "GAUGE","step": 60}
	payload.append(copy.copy(item1))
	payload.append(copy.copy(item2))
	payload.append(copy.copy(item3))

#执行cmd获得想要的结果loss_rate max_time average_time
def cmd_get_res(ping_dict):
	print ping_dict
	URL = ping_dict['args_url']

        if ( ping_dict['args_ipversion'] == 0 ):
                ping_dict['args_ipversion'] = "ping"
                VERSION = 'ipv4'
        else:
                ping_dict['args_ipversion'] = "ping6"
                VERSION = 'ipv6'

    cmd = "{0} -s {1} -c {2} -W {3} -q {4} ".format(ping_dict['args_ipversion'],ping_dict['args_packagesize'],ping_dict['args_count'],ping_dict['args_timeout'],ping_dict['args_url'])
	print cmd
    status ,output = commands.getstatusoutput(cmd)
#	print output
#	print status

	if (status == 512):
		print URL+" <==== We dont know this host !!!"
		return 512
	elif (status == 256):
		print URL+" <==== We cant reach this host !!!"
		return 256
	elif (status == 0):
	        temp1 = re.search(r"received, \d+\.?\d{0,3}% packet loss",output)
#		print temp1.group()
	        temp2 = re.search(r"\d+\.?\d{0,3}\/\d+\.?\d{0,3}\/\d+\.?\d{0,3}\/",output)
#		print temp2.group()
        	
		t1 = re.findall(r"\d+\.?\d{0,3}", temp1.group())
#		print t1
		t2 = re.findall(r"\d+\.?\d{0,3}", temp2.group())
#		print t2
		res = []
        	res.append(t1[0])
        	res.append(t2[2])
        	res.append(t2[1])
#		print res
		return  res


#把参数list传入到load函数进行处理
def load_pingargs(ping_dict):
        res=cmd_get_res(ping_dict)
        load_data(ping_dict,res)

#获取ping 的参数list
def getconfig():
    	f = open("/opt/ping-args.json","r")
    	pingargs = f.read()
    	pingargs = json.loads(pingargs)
    	return pingargs


if __name__ == '__main__':
	push_url = "http://127.0.0.1:1988/v1/push"
	process = 8
#	pinglists = [{"args_count": 4,"args_id": 1,"args_packagesize": 64,"args_timeout": 2,"args_url": "www.172.com","args_ipversion": 0},{"args_count": 4,"args_id": 2,"args_packagesize": 64,"args_timeout": 2,"args_url": "www.173.com","args_ipversion": 0},{"args_count": 4,"args_id": 3,"args_packagesize": 64,"args_timeout": 2,"args_url": "www.176.com","args_ipversion": 0}]
#获取ping的参数list
	pinglists = getconfig()
	#print pinglists
#定义一个payload，以便全局使用，和后面的post
	payload = []
	
#	print pinglists
	pool = ThreadPool(process)

	for pingargs in pinglists:
#		print pingargs
		pool.apply_async(load_pingargs, args=(pingargs,))

	pool.close()
	pool.join()
#把payloadpost出去
	print payload
	r = requests.post(push_url, data=json.dumps(payload))
