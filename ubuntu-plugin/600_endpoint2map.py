#!/usr/bin/python3
#coding=utf-8

import time
import requests
# pip install requests
import json
# import urlparse  
import subprocess as commands
import config

def get_Apitoken(name, password, api_addr):
    d = {
        "name": name, "password": password,
    }

    h = {"Content-type":"application/json"}

    r = requests.post("%s/user/login" %(api_addr,), \
            data=json.dumps(d), headers=h)

    if r.status_code != 200:
        raise Exception("%s %s" %(r.status_code, r.text))

    sig = json.loads(r.text)["sig"]
    return json.dumps({"name":name,"sig":sig})

def get_History(Apitoken, Data, api_addr):
    h = {
         "Apitoken": Apitoken ,
	 "X-Forwarded-For":"127.0.0.1" 
        }


    r = requests.get("%s/graph/endpoint" %(api_addr,), \
           params= Data , headers=h)

    if r.status_code != 200:
        raise Exception("%s %s" %(r.status_code, r.text))

    return r.text


def get_EndpointName():
    cmdline = "uname -n"
    status,UNAME = commands.getstatusoutput(cmdline)    
    return UNAME


if __name__ == '__main__':
    api_addr = "http://{}:8080/api/v1".format(config.falcon_config['api_ip'])
    api_push = "http://{}:3456".format(config.falcon_config['api_ip'])
    name = config.falcon_config['name']
    password = config.falcon_config['password']
	

    uname = get_EndpointName() 

    d = {
	"limit":10,
	"q": uname
	
	}

    try:
	#api_addr=url_add_params(api_addr,q=a.+)
        Apitoken = get_Apitoken(name, password, api_addr)
        print(Apitoken)
        res = get_History(Apitoken, d, api_addr)
    	
        res = json.loads(res)
        print(res)
        print(res[0]['endpoint'])
        print(res[0]['id'])
	
        endpoint_name = res[0]['endpoint']
        endpoint_id   = res[0]['id']
        
        post_url = "{}/api/push/{}/{}/".format(api_push,endpoint_name,endpoint_id)
        print(post_url)
        r = requests.get(post_url)
        print(r.text)


    except Exception as e:
        print(e)

