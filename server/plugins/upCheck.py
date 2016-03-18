#coding=utf8
from conf.services.Linux import upCheck
from mymail.sendMail import MailServer
def monitor_alarm(data=None,flag=None):
    if data is not None and flag == 'upCheck':
        level       = upCheck()
        hostip      = "{0}_{1}" .format(data['hostip'],data['hostname'])
        last_time   = data['last_time']

        uptime_result = data['uptime_result']
        M_1,M_5,M_15  = uptime_result.split('\n')[0].split(':')[-1].split(',')   #获取过去1分钟,5分钟,10分钟的负载
        Cpu_num       = uptime_result.split('\n')[1]                         #get cpu num
        alerm_level   = None

        uptime_Level_1 = level.level_dic['uptime_Level'][1]  #the wronging is leve one
        uptime_Level_2 = level.level_dic['uptime_Level'][2]  #the wronging is leve two

        if uptime_Level_1 <= float(M_1) < uptime_Level_2:
            alerm_level = 1
        elif float(M_1) >= uptime_Level_2:
            alerm_level = 2
        else:
            return 0

        if alerm_level is not None:
            alerm_data    = "当前负载:{0}\n5分钟:{1}\n15分钟:{2}\n服务器核心数量:{3}" .format(M_1,M_5,M_15,Cpu_num)
            newMailServer = MailServer()
            title,content = newMailServer.mail_content(flag,alerm_level,hostip,last_time,alerm_data)
            newMailServer.send_mail(content,mail_title=title)
    else:
        raise "paraments is not success!" 
