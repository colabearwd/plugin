#!/usr/bin/python
#coding=utf-8


import commands
import time
import copy
import json
import requests
import re
from multiprocessing.dummy import Pool as ThreadPool

def load_data(curl_dict,res):
        
	URL = curl_dict['args_url']
        if ( curl_dict['args_ipversion'] == 0 ):
                VERSION = 'curl4'
        else:
                VERSION = 'curl6'
        getuname = "uname -n"
        status ,UNAME = commands.getstatusoutput(getuname)
        ts = int(time.time())
        item1 = {"metric": "http_code","endpoint":UNAME,"tags":"target="+URL+",ip-version="+VERSION,"value":res[0],"timestamp":ts,"counterType":"GAUGE","step":60}
        item2 = {"metric": "http_connect","endpoint": UNAME,"tags": "target="+URL+",ip-version="+VERSION,"value": res[1],"timestamp": ts,"counterType": "GAUGE","step": 60}
        item3 = {"metric": "time_namelookup","endpoint": UNAME,"tags": "target="+URL+",ip-version="+VERSION,"value": res[2],"timestamp": ts,"counterType": "GAUGE","step": 60}
        item4 = {"metric": "time_redirect","endpoisnt": UNAME,"tags": "target="+URL+",ip-version="+VERSION,"value": res[3],"timestamp": ts,"counterType": "GAUGE","step": 60}
        item5 = {"metric": "time_pretransfer","endpoint": UNAME,"tags": "target="+URL+",ip-version="+VERSION,"value": res[4],"timestamp": ts,"counterType": "GAUGE","step": 60}
        item6 = {"metric": "time_connect","endpoint": UNAME,"tags": "target="+URL+",ip-version="+VERSION,"value": res[5],"timestamp": ts,"counterType": "GAUGE","step": 60}
        item7 = {"metric": "time_starttransfer","endpoint": UNAME,"tags": "target="+URL+",ip-version="+VERSION,"value": res[6],"timestamp": ts,"counterType": "GAUGE","step": 60}
        item8 = {"metric": "time_total","endpoint": UNAME,"tags": "target="+URL+",ip-version="+VERSION,"value": res[7],"timestamp": ts,"counterType": "GAUGE","step": 60}
        item9 = {"metric": "speed_download","endpoint": UNAME,"tags": "target="+URL+",ip-version="+VERSION,"value":res[8],"timestamp": ts,"counterType": "GAUGE","step": 60}
        payload.append(copy.copy(item1))
        payload.append(copy.copy(item2))
        payload.append(copy.copy(item3))
        payload.append(copy.copy(item4))
        payload.append(copy.copy(item5))
        payload.append(copy.copy(item6))
        payload.append(copy.copy(item7))
        payload.append(copy.copy(item8))
        payload.append(copy.copy(item9))


def cmd_get_res(curl_dict):

#	print curl_dict
        if ( curl_dict['args_ipversion'] == 0 ):
                curl_dict['args_ipversion'] = "4"
                VERSION = 'curl4'
        else:
                curl_dict['args_ipversion'] = "6"
                VERSION = 'curl6'

        curl_dict['args_timeout']=str(curl_dict['args_timeout'])


        cmd = "curl -"+ curl_dict['args_ipversion']+" -o /dev/null --connect-timeout "+curl_dict['args_timeout']+" -s -w %{http_code}:%{http_connect}:%{time_namelookup}:%{time_redirect}:%{time_pretransfer}:%{time_connect}:%{time_starttransfer}:%{time_total}:%{speed_download} "+curl_dict['args_url']
       print cmd
        status ,output = commands.getstatusoutput(cmd)
 #       print output
	return output.split(":")



def load_curlargs(curl_dict):
#	print curl_dict
        res=cmd_get_res(curl_dict)
#	print res
        load_data(curl_dict,res)


def getconfig():
        f = open("/opt/curl-args.json","r")
        curlargs = f.read()
        curlargs = json.loads(curlargs)
        return curlargs


if __name__ == '__main__':
        push_url = "http://127.0.0.1:1988/v1/push"
        process = 8
#       pinglists = [{"args_count": 4,"args_id": 1,"args_packagesize": 64,"args_timeout": 2,"args_url": "www.172.com","args_ipversion": 0},{"args_count": 4,"args_id": 2,"args_packagesize": 64,"args_timeout": 2,"args_url": "www.173.com","args_ipversion": 0},{"args_count": 4,"args_id": 3,"args_packagesize": 64,"args_timeout": 2,"args_url": "www.176.com","args_ipversion": 0}]

        curllists = getconfig()
        print curllists

        payload = []

#       print pinglists
        pool = ThreadPool(process)

        for curlargs in curllists:
#               print pingargs
                pool.apply_async(load_curlargs, args=(curlargs,))

        pool.close()
        pool.join()

        print payload
        r = requests.post(push_url, data=json.dumps(payload))
