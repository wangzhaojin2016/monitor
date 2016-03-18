#coding=utf8
from conf.services.Linux import processing
from mymail.sendMail import MailServer
def monitor_alarm(data=None,flag=None):
    if data is not None and flag == 'processing':
        hostip      = "{0}_{1}" .format(data['hostip'],data['hostname'])
        last_time   = data['last_time']
        alerm_level = 1

        alerm_data = {}
        failedport = []
        for processName,statusList in data.iteritems():
            if processName not in ['hostip','hostname','last_time']:
                for status in statusList:
                    if status != 'OK':
                        failedport.append(status)
                        alerm_data[processName] = failedport

        if len(alerm_data.keys()) != 0:
            for key,value in alerm_data.iteritems():
                alerm_data = "\n"
                alerm_data += "{0}进程异常,端口:{1}" .format(key,value)


            newMailServer = MailServer()
            title,content = newMailServer.mail_content(flag,alerm_level,hostip,last_time,alerm_data)
            newMailServer.send_mail(content,mail_title=title)
    else:
        raise "paraments is not success!"
