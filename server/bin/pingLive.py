#coding=utf8
import os
import sys
import time
import commands
import threading
import get_path
import MySQLdb
from conf.monitor_config import *
from mymail.sendMail import MailServer

value_dic = {}
def Ping(dest_host=[]):
    for num,ip in enumerate(dest_host):
        print num,ip
        cmd = "ping -c 3 {0}| grep received".format(ip)
        status,result = commands.getstatusoutput(cmd)
        if status != 0:
            value_dic[ip] = {"status":status}
        else:
            list = result.split(',')
            if len(list) == 4:list.insert(2,"0 error")
            value_dic[ip] = {"status":status,
                         "receivedNum":list[1],
                         "error":list[2],
                         "lose":list[3],
                         "time":list[4]
                         }
    return value_dic

def exec_sql(sql=None):
    if exec_sql is None:
        raise "parents is wrong"
    db = MySQLdb.connect(user=DB_USER,db=DB_NAME,passwd=DB_PASSWORD,host=DB_HOST,charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    result = cursor.fetchall()
    return result
    
def getHost():
    sql = "select id,host from monitor_hostinfo"
    result = exec_sql(sql)
    ip = []
    for i in result:
        ip.append(i[1])
    return ip
def get_start_nums():
    sql = "select host,start_nums from monitor_start_nums"
    result = exec_sql(sql)
    start_nums_dic = {}
    if result:
        for i in result:
            start_nums_dic[i[0]] = i[1]
    return start_nums_dic

def get_start_time():
    sql = "select host,start_time from monitor_start_time"
    result = exec_sql(sql)
    start_time_dic = {}
    if result:
        for i in result:
            start_time_dic[i[0]] = i[1]
    return start_time_dic 

def set_start_nums(ip,start_nums):
    sql = "update monitor_start_nums set start_nums='{0}' where host='{1}'".format(start_nums,ip)
    try:
        exec_sql(sql)
        return 1
    except Exception,e:
        print e
        return 0

def set_start_time(ip,start_time):
    sql = "update monitor_start_time set start_time='{0}' where host='{1}'".format(start_time,ip)
    try:
        exec_sql(sql)
        return 1
    except Exception,e:
        print e
        return 0

def add_start_nums(ip,start_nums):
    sql = "insert into monitor_start_nums(host,start_nums) values('{0}','{1}')".format(ip,start_nums)
    try:
        exec_sql(sql)
        return 1
    except Exception,e:
        print e
        return 0

def add_start_time(ip,start_time):
    sql = "insert into monitor_start_time(host,start_time) values('{0}','{1}')".format(ip,start_time)
    try:
        exec_sql(sql)
        return 1
    except Exception,e:
        print e
        return 0

def addHost(ip):
    iplist = getHost()
    if ip in iplist:return 0
    sql = "insert into monitor_hostinfo(host) values('{0}')".format(ip)
    try:
        exec_sql(sql)
    except :
        print "insert sql type error|| [{0}]".format(sql)
        return "1"

def Monitor(value,flag='Ping Failed',alerm_level=2):
    value_xx = value
    last_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    monitor_ip = []
    monitor_start_time = get_start_time()
    monitor_nums = get_start_nums()
    alerm_data = ''
    for ip,info in value_xx.iteritems():
        ip = str(ip)
        if ip not in monitor_start_time.keys():
            add_start_time(ip,'')
        if ip not in monitor_nums.keys():
            add_start_nums(ip,0)
        if int(info['receivedNum'].split()[0]) != 3:
            alerm_data += '\n'
            alerm_data += ip + info['receivedNum']
            monitor_ip.append(ip)
            if monitor_start_time.get(ip,None) and  monitor_start_time[ip]:
                start_time = monitor_start_time[ip]
            else:
                set_start_time(ip,last_time)
                start_time = last_time

            alerm_data += '\n监控告警开始时间:{0}'.format(start_time)
            if not monitor_nums.get(ip,None):
                set_start_nums(ip,1)
                start_num = 1
            else:
                if int(monitor_nums[ip]):
                    nums = int(monitor_nums[ip]) + 1
                    set_start_nums(ip,nums)
                    monitor_nums[ip] = nums
                else: set_start_nums(ip,1)
                start_num = monitor_nums[ip]
            alerm_data += '\n监控告警连续告警次数:{0}'.format(start_num)
        else:
            set_start_time(ip,'')
            set_start_nums(ip,0)
    
    if monitor_ip:
        monitor_nums = get_start_nums()
        for key,ip in enumerate(monitor_ip):
            ip = str(ip)
            if 0 < int(monitor_nums[ip]) <= 6 or int(monitor_nums[ip]) % 15 == 0:
                newMailServer = MailServer()
                title,content = newMailServer.mail_content(flag,alerm_level,';'.join(monitor_ip),last_time,alerm_data)
                newMailServer.send_mail(content,mail_title=title)

if __name__ == '__main__':
    while 1:
        iplist = getHost()
        t = threading.Thread(target=Ping,args=(iplist,))
        t.start()
        t.join()
        Monitor(value_dic)
        print "[{0}]Ping Monitor".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        time.sleep(100)
