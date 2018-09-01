#!/usr/bin/python
# coding=utf-8


import commands
import time
import copy
import json
import requests
import re
from multiprocessing.dummy import Pool as ThreadPool


def load_data(curl_dict, res):
    """
    传入参数字典和结果列表
    将数据封装成列表
    """
    URL = curl_dict['args_url']
    if (curl_dict['args_ipversion'] == '4' ):
        VERSION = 'curl4'
    else:
        VERSION = 'curl6'
    getuname = "uname -n"
    status, UNAME = commands.getstatusoutput(getuname)
    ts = int(time.time())
    metriclist = ['http_code','http_connect','time_namelookup','time_redirect','time_pretransfer','time_connect','time_starttransfer','time_total','speed_download']

    for (metric, re) in zip(metriclist, res):
        item = {"metric": metric, "endpoint": UNAME, "tags": "target="+URL+",ip-version=" +
                VERSION, "value": re, "timestamp": ts, "counterType": "GAUGE", "step": 60}
        payload.append(copy.copy(item))
        print item



def cmd_get_res(curl_dict):
    """
    传入对cmd的命令进行控制的参数字典
    使用cmd命令，获取到结果，并返回
    """
    if (curl_dict['args_ipversion'] == 0):
        curl_dict['args_ipversion'] = "4"
    else:
        curl_dict['args_ipversion'] = "6"

    curl_dict['args_timeout'] = str(curl_dict['args_timeout'])

    cmd = "curl -" + curl_dict['args_ipversion']+" -o /dev/null --connect-timeout "+curl_dict['args_timeout'] + " -s -w %{http_code}:%{http_connect}:%{time_namelookup}:%{time_redirect}:%{time_pretransfer}:%{time_connect}:%{time_starttransfer}:%{time_total}:%{speed_download} " + curl_dict['args_url']
    
    print cmd
    status, output = commands.getstatusoutput(cmd)

    return output.split(":")


def curl_exe_group(curl_dict):
    """
    多线程需要执行的函数group
    """
    res = cmd_get_res(curl_dict)

    load_data(curl_dict, res)


def getconfig():
    """
    获得curl需要的参数列表，并把参数列表放在文件中，在 /opt 文件夹下
    """
    f = open("/opt/curl-args-demo.json", "r")
    curlargs = f.read()
    curlargs = json.loads(curlargs)
    return curlargs


if __name__ == '__main__':
    """
    设置需要传送数据到哪个ip：port
    多线程运行配置文件列表中的文件
    """
    push_url = "http://127.0.0.1:1988/v1/push"
    process = 8
    curllists = getconfig()
    print curllists

    payload = []

    pool = ThreadPool(process)

    for curlargs in curllists:

        pool.apply_async(curl_exe_group, args=(curlargs,))

    pool.close()
    pool.join()

#    print payload
    r = requests.post(push_url, data=json.dumps(payload))

