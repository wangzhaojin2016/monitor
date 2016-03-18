#coding=utf8
import os
import sys
import socket
import time
import json


curdir = os.path.dirname(os.path.abspath(__file__))
curpath = sys.path.append(os.path.abspath(os.path.join(curdir,'../')))
from conf.config import *
from conf.service import enabled_services

def send_status_data(action=None,status_data=None):
    if action is not None and status_data is not None:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((MASTER_HOST,MASTER_PORT))
    else:
        raise ValueError("Need two arguments")

    #user_input = raw_input("You msg:").strip()
    if action == 'SendMonitorData':
        s.send("SendMonitorData")
        server_confirmation = s.recv(1024)
        if server_confirmation == 'ReadyToReceive':
            s.sendall(status_data)
    data = s.recv(1024)
    s.close()

monitor_dic = {}
hostname = socket.gethostname()
for k,v in enabled_services.items():
    if k == 'service':
        for s_name,s_api in v.items():
            monitor_dic[s_name] = {
                "last_check":0,
                "interval":s_api.interval
            }

while 1:
    status_dic={}
    for service_name,value_dic in monitor_dic.items():
        if time.time() - value_dic['last_check'] >= value_dic['interval']:
            status_dic[service_name] = enabled_services['service'][service_name].plugin.monitor(hostname)
            value_dic['last_check'] = time.time()
    if len(status_dic) > 0:
        #send data
        try:
            send_status_data("SendMonitorData",json.dumps(status_dic))
            print "[{0}] send data".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        except Exception,e:
            print e
            print "[{0}]连接监控中心出错,请检查socket连接".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            time.sleep(20)
            continue
    time.sleep(2)
