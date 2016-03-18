#coding=utf8
from conf.services.Linux import cpu
from mymail.sendMail import MailServer

def monitor_alarm(data=None,flag=None):
    if data is not None and flag == 'cpu':
        level = cpu()
        iowait     = float(data['iowait'])
        system_use = float(data['system'])
        idle       = float(data['idle'])
        hostip     = "{0}_{1}" .format(data['hostip'],data['hostname'])
        last_time  = data['last_time']
        alerm_level = None

        level_iowait_one = level.level_dic['iowait'][1] #the wring is one
        level_iowait_two = level.level_dic['iowait'][2] #the wring is two
        level_system_one = level.level_dic['system'][1]
        level_system_two = level.level_dic['system'][2]
        level_idle_one   = level.level_dic['idle'][1]
        level_idle_two   = level.level_dic['idle'][2]

        iowait_check_1 = level_iowait_one <= iowait < level_iowait_two
        iowait_check_2 = iowait >=level_iowait_two
        system_check_1 = level_system_one <= system_use < level_system_two
        system_check_2 = system_use >= level_system_two
        idle_check_1   = level_idle_two <= idle < level_idle_one
        idle_check_2   = idle <= level_idle_two

        if iowait_check_1 or system_check_1 or idle_check_1:
            alerm_level = 1
        elif iowait_check_2 or system_check_2 or idle_check_2:
            alerm_level = 2
        else:
           return 0 
            
        if alerm_level is not None:
            newMailServer = MailServer()
            title,content = newMailServer.mail_content(flag,alerm_level,hostip,last_time,data)
            newMailServer .send_mail(content,mail_title=title)


    else:
        raise "paraments is not success!"
