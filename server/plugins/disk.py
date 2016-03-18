#coding=utf8
from conf.services.Linux import disk
from mymail.sendMail import MailServer
def monitor_alarm(data=None,flag=None):
    if data is not None and flag == 'disk':
        level       = disk()
        hostip      = "{0}_{1}" .format(data['hostip'],data['hostname'])
        last_time   = data['last_time']
        alerm_level = 1

        level_disk = level.level_dic['DiskUse'][1] #while disk percentage > 90%
        alerm_data = {}
        for key,value in data.iteritems():
            if key in ['/','/data']:
                percent   = int(value[4].strip('%'))
                if percent >= level_disk:
                    alerm_data[key] = value 
        if alerm_data:
            default_data = ''
            for i in alerm_data.values():
                default_data += "\n"
                default_data += '   |   '.join((' '.join(i)).split())
            Filesystem = ' | '.join(data['Filesystem'])
            alerm_data = "{0}{1}".format(Filesystem,default_data)
            newMailServer = MailServer()
            title,content = newMailServer.mail_content(flag,alerm_level,hostip,last_time,alerm_data)
            newMailServer.send_mail(content,mail_title=title)

    else:
        raise "paraments is not success!"
