#!/usr/bin/python
# coding=utf-8

# TODO-当修改了数据库，需要修改本文的args_ipversion

import commands
import time
import copy
import json
import requests
import re
from multiprocessing.dummy import Pool as ThreadPool


def load_data(ping_dict, res):
    """
    传入参数字典和结果列表
    将数据封装成列表   
    """
    loss_rate = res[0]
    max_time = res[1]
    average_time = res[2]
    URL = ping_dict['args_url']
    if (ping_dict['args_ipversion'] == "ping"):
        VERSION = 'ipv4'
    else:
        VERSION = 'ipv6'
    getuname = "uname -n"
    status, UNAME = commands.getstatusoutput(getuname)
    ts = int(time.time())
    metriclist = ['ping.loss_rate', 'ping.max_time', 'ping.average_time']

    for (metric, re) in zip(metriclist, res):
        item = {"metric": metric, "endpoint": UNAME, "tags": "target="+URL+",ip-version=" +
                VERSION, "value": re, "timestamp": ts, "counterType": "GAUGE", "step": 60}
        payload.append(copy.copy(item))
        print item



def cmd_get_res(ping_dict):
    """
    传入对cmd的命令进行控制的参数字典
    使用cmd命令，获取到结果，并返回   
    """
    print ping_dict
    URL = ping_dict['args_url']

    if (ping_dict['args_ipversion'] == 0):
        ping_dict['args_ipversion'] = "ping"
        VERSION = 'ipv4'
    else:
        ping_dict['args_ipversion'] = "ping6"
        VERSION = 'ipv6'

    cmd = "{0} -s {1} -c {2} -W {3} -q {4} ".format(ping_dict['args_ipversion'], ping_dict['args_packagesize'],
                                                    ping_dict['args_count'], ping_dict['args_timeout'], ping_dict['args_url'])
    print cmd
    status, output = commands.getstatusoutput(cmd)

    if (status == 512):
        print URL+" <==== We dont know this host !!!"
        res = [-1, -1, -1]
        return res

    elif (status == 256):
        print URL+" <==== We cant reach this host !!!"
        res = [-2, -2, -2]
        return res

    elif (status == 0):
        temp1 = re.search(r"received, \d+\.?\d{0,3}% packet loss", output)

        temp2 = re.search(
            r"\d+\.?\d{0,3}\/\d+\.?\d{0,3}\/\d+\.?\d{0,3}\/", output)


        t1 = re.findall(r"\d+\.?\d{0,3}", temp1.group())

        t2 = re.findall(r"\d+\.?\d{0,3}", temp2.group())

        res = []
        res.append(t1[0])
        res.append(t2[2])
        res.append(t2[1])

        return res



def ping_exe_group(ping_dict):
    """
    多线程需要执行的函数group   
    """
    res = cmd_get_res(ping_dict)
    load_data(ping_dict, res)


def getconfig():
    """
    获得curl需要的参数列表，并把参数列表放在文件中，在 /opt 文件夹下    
    """
    f = open("/opt/ping-args-demo.json", "r")
    pingargs = f.read()
    pingargs = json.loads(pingargs)
    return pingargs


if __name__ == '__main__':
    """
    设置需要传送数据到哪个ip：port
    多线程运行配置文件列表中的文件    
    """
    push_url = "http://127.0.0.1:1988/v1/push"
    process = 8

    pinglists = getconfig()

    payload = []


    pool = ThreadPool(process)

    for pingargs in pinglists:

        pool.apply_async(ping_exe_group, args=(pingargs,))

    pool.close()
    pool.join()

#    print payload
    r = requests.post(push_url, data=json.dumps(payload))

