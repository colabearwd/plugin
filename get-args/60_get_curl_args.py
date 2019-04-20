#!/usr/bin/python

import types
#import urllib2
import json
import requests
import sys
sys.path.append("..")
import config

def getUrlJson():
    try:
        push_url = "http://{}:3456/api/curl".format(config.falcon_config['api_ip'])
        data1 = requests.get(push_url)
    #       print data1.text

        return data1.text
    except Exception as e:
        print(e)


def write2file(res):
    print(res)
    #res = json.dumps(res)

    # print(json_res)
    fp = open("/opt/curl-args-demo.json", "w")
    fp.write(res)
    fp.close()


if __name__ == "__main__":

    data = getUrlJson()
    write2file(data)
    print(data)
