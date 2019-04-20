#!/usr/bin/python

import time
import requests
import json
import pymysql


name = "root"
password = "root"
api_addr = "http://1.1.1.1:8080/api/v1"


config={
    "host":"127.0.0.1",
    "user":"mysql_account",
    "password":"mysql_passwd",
    "database":"mysql_database"
}



def insert_data(res_list):


    for re in res_list:
        print(re)

    db = pymysql.connect(**config)
    cursor = db.cursor()

    for re in res_list:
        sql = "INSERT INTO `myproject`.`curl_res`(`curl_endpoint`, `curl_ipversion`, `curl_targeturl`, `curl_timestamp`, `curl_value`) VALUES (%s, %s, %s, %s, %s)"
        # cursor.execute(sql,(re['endpoint'],re['']  ))
        # print(re['endpoint'])
        # print(re['counter'][27:32])
        # print(re['counter'][40:])
        # print(re['Values'][0]['timestamp'])
        # print(re['Values'][0]['value'])
        temp=(re['Values'][0]['value'])
        temp1= temp*100
        # print(temp1)
        cursor.execute(sql, (re['endpoint'],re['counter'][27:32], re['counter'][40:],re['Values'][0]['timestamp'],temp1))

    db.commit()
    cursor.close()
    db.close()


def get_Apitoken(name, password, api_addr):
    d = {
        "name": name, "password": password,
    }

    h = {"Content-type":"application/json"}

    r = requests.post("%s/user/login" %(api_addr,), data=json.dumps(d), headers=h)

    if r.status_code != 200:
        raise Exception("%s %s" %(r.status_code, r.text))

    sig = json.loads(r.text)["sig"]
    return json.dumps({"name":name,"sig":sig})


def get_list(flag):
    # 0 get all namelist
    # 1 get all eidlist
    print(Apitoken)

    h = {
        "Apitoken": Apitoken,
        "X-Forwarded-For": "1.1.1.1"
    }

    d = {
        "q": "."
    }

    r = requests.get("%s/graph/endpoint" % (api_addr,), params=d, headers=h)

    if r.status_code != 200:
        raise Exception("%s %s" % (r.status_code, r.text))

    namelist = []
    eidlist = []

    res = json.loads(r.text)
    for re in res:
        namelist.append(re['endpoint'])
        eidlist.append(re['id'])

    # print(namelist)
    # print(eidlist)
    if(flag == 0):
        res = namelist
    else:
        res = eidlist

    return res


def get_endpoint_counter(eidlist, metriclist):
    # get all
    #     {
    #     "counter": "ping.average_time/ip-version=ipv4,target=www.114.com",
    #     "endpoint_id": 1,
    #     "step": 60,
    #     "type": "GAUGE"
    # },
    # {
    #     "counter": "ping.average_time/ip-version=ipv4,target=www.126.com",
    #     "endpoint_id": 1,
    #     "step": 60,
    #     "type": "GAUGE"
    # },

    print(Apitoken)
    d = {
        "eid": eidlist,
        "metricQuery": metriclist
    }
    h = {
        "Apitoken": Apitoken,
        "X-Forwarded-For": "1.1.1.1"
    }
    r = requests.get("%s/graph/endpoint_counter" % (api_addr,), params=d, headers=h)
    if r.status_code != 200:
        raise Exception("%s %s" % (r.status_code, r.text))

    return r.text


def get_counterlist(counterindex):

    eidlist = get_list(1)
    eidlist = ','.join('%s' %eid for eid in eidlist)


    res = get_endpoint_counter(eidlist,counterindex)

    res = json.loads(res)
    counterlist = []

    for re in res:
        counterlist.append(re['counter'])

    return counterlist


def func2():
    # print(Apitoken)
    h = {
        "Apitoken": Apitoken,
        "Content-type": "application/json;charset=utf-8",
        "X-Forwarded-For": "1.1.1.1"
    }
    namelist = get_list(0)
    print(namelist)
    counterlist = get_counterlist("curl.time_total")

    temp=[]
    for re in counterlist:
        if re not in temp:
            temp.append(re)

    counterlist = temp
    print(counterlist)

    #get ping-averagetime
    end_time = int(time.time())
    start_time = end_time - 120

    # print (namelist)

    data = {
         "step": 60,

         "start_time": start_time,

         "hostnames": namelist,

         "end_time": end_time,

         "counters": counterlist,

         "consol_fun": "AVERAGE"

        }

    r = requests.post("%s/graph/history" % (api_addr,), data=json.dumps(data), headers=h)
    if r.status_code != 200:
        raise Exception("%s %s" % (r.status_code, r.text))
    res = json.loads(r.text)
    tmp_list = []

    for re in res:
        if re['Values']:
            for r1 in re['Values']:
                if r1['value'] != None:
                    tmp_list.append(re)
                    print(re)

    res_list = []
    for res in tmp_list:
        if res not in res_list:
            res_list.append(res)

    insert_data(res_list)



    # value = []
    # flag = []
    # dict = {}
    # count =0
    # for re in res_list:
    #     value.append(re['Values'][0]['value'])
    #     flag.append(count)
    #     dict[count]=re
    #     count += 1
    #     print(re['Values'][0]['value'])


if __name__ == '__main__':
    Apitoken=get_Apitoken(name,password,api_addr)
    print(Apitoken)
    func2()
