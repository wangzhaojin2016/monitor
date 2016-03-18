#coding=utf8
from conf.services.Linux import memory
from mymail.sendMail import MailServer
def monitor_alarm(data=None,flag=None):
    if data is not None and flag == 'memory':
        level       = memory()
        hostip      = "{0}_{1}" .format(data['hostip'],data['hostname'])
        last_time   = data['last_time']
        nowMemUsage_p  = data['MemUsage_p']
        alerm_level = None

        MemUsage_p_1 = level.level_dic['MemUsage_p'][1] #the wring is one
        MemUsage_p_2 = level.level_dic['MemUsage_p'][2] #the wring is one

        if MemUsage_p_1 <= nowMemUsage_p < MemUsage_p_2:
            alerm_level = 1
        elif nowMemUsage_p >= MemUsage_p_2:
            alerm_level = 2
        else:
            return 0

        alerm_data = {}
        for key,value in data.iteritems():
            if key not in ['status','hostip','last_time']:
                alerm_data[key] = value

        #summary_info = "Memory Use:{0}%\nSwap Use:{1}%" .format(str(data['MemUsage_p']),str(data['SwapUsage_P']))
        #alerm_data = "{0}\n{1}".format(' '.join(summary_info.split()),alerm_data)
        summary_info = "内存使用:{0}%\nSWAP使用:{1}%" .format(str(data['MemUsage_p']),str(data['SwapUsage_P']))
        alerm_data = "{0}\n{1}".format(summary_info,alerm_data)
        
        if alerm_level is not None:
            newMailServer = MailServer()
            title,content = newMailServer.mail_content(flag,alerm_level,hostip,last_time,alerm_data)
            newMailServer .send_mail(content,mail_title=title)

    else:
        raise "paraments is not success!"
