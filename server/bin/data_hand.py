#coding=utf8
import time
import socket
import json
import get_path
import redis_connector as Redis
from conf.templates import enabled_templates
from conf.monitor_config import PORT
from get_monitor_index_dic import monitor_host_dic

def send_status_data(action,status_data):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('127.0.0.1',PORT))
    #user_input = raw_input("You msg:").strip()
    if action == 'pushDataIntoRedis':
        s.send("pushDataIntoRedis")
        server_confirmation = s.recv(1024)
        if server_confirmation == 'pushComplate':
            print '---------connecting redis to pull tp data-----------'
            status_dic = Redis.r.get('STATUS_DATA')
    s.close()
    return status_dic

while 1:
    last_status_dic = send_status_data('pushDataIntoRedis','')
    if last_status_dic is not None:
        last_status_dic = json.loads(last_status_dic)
        for host_name,template_num in monitor_host_dic.items():
            print host_name,template_num
            if last_status_dic.has_key(host_name):
                print last_status_dic[host_name]
            else:
                print "avalied data from %s in DB" % host_name
    else:
        print '出事了'
    time.sleep(10)