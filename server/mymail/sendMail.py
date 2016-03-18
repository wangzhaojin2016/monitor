#coding=utf-8
'''
发送txt文本邮件
'''
import smtplib  
from email.mime.text import MIMEText
from mail_config import *

class MailServer(object): 
    def send_mail(self,mail_content,mail_to_list=mail_to_list,mail_title=mail_title):
        """
        exaple:
            sendmail(mail_content,mail_to_list=None,mail_title=None)
                     告警内容,邮件接收人,邮件主题
            this function need one argument
            eg:
                sendmail("Hello")
        """ 
        msg = MIMEText(mail_content,_subtype='plain',_charset='utf8')  
        msg['Subject'] = mail_title  
        msg['From']    = mail_user  
        msg['To']      = ";".join(mail_to_list)  
        try:  
            server = smtplib.SMTP()
            server.connect(mail_host)  
            server.login(mail_user,mail_pass)  
            server.sendmail(mail_user, mail_to_list, msg.as_string())  
            server.close()  
            return True  
        except Exception, e:  
            print str(e)  
            return False  

    def mail_content(self,alerm_name,alerm_level,hostip,last_time,alerm_data,mail_title=mail_title):
        """
        eg:
        mail_content(告警名称,告警等级,告警IP,告警时间,告警内容,主题=default(mail_title))
        """
        title   = "{0}:{1}告警 --[告警等级:{2},主机IP:{3},时间:{4}]" .format(mail_title,alerm_name,alerm_level,hostip,last_time)
        content = "[告警等级]:{0}\n[主机IP]:{1}\n\n[详细信息]:\n{2}" .format(alerm_level,hostip,alerm_data)
        return title,content

if __name__ == '__main__':  
    mailserver = MailServer()
    if mailserver.send_mail("hello world！"):  
        print "发送成功"  
    else:  
        print "发送失败" 
