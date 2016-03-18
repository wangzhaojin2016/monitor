import os
import sys
import time
import json
import commands
import get_path
#import SocketServer
from SocketServer import (TCPServer as TCP,BaseRequestHandler as SRH,ForkingMixIn as FMI)

from conf.monitor_config import *
from monitor_check import MonitorListCheck
#import redis_connector as Redis

class tcpServer(TCP,FMI):
    pass



class MyTCPHander(SRH):
    """
    The RequestHandler class for our server.
    it is instantiated once per connection to the server ,
    and mustoverride the handle() method to implement communication to the client
    """
    def alarm(self,client_IP=None,value_dic=None):
        if value_dic is None:
            pass
        else:
            for key,value in value_dic.iteritems():
                value['hostip'] = client_IP
                nowtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                value['last_time'] = nowtime

                ################get plugins arlm##################
                MonitorListCheck[key].plugin.monitor_alarm(value,key)

    def handle(self):
        client_IP = self.client_address[0]
        print "[{0}]got a connection from:{1}".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),client_IP)
        data = self.request.recv(1024)
        if data == 'SendMonitorData':
            self.request.send("ReadyToReceive")
            value_dic = json.loads(self.request.recv(8192))
            self.alarm(client_IP,value_dic)  #get function alarm
            self.request.send('SendMonitorData complate')
        elif data == 'pushDataIntoRedis':
            Redis.r['STATUS_DATA'] = json.dumps(value_dic)
            #Redis.r.set()
            print '-------------------going to save data into redis------------------'
            self.request.send('pushComplate')

  
if __name__ == '__main__':
    #Create the server,binding to localhost on port 9999
    server = tcpServer(('0.0.0.0',PORT),MyTCPHander)
    server.serve_forever()
    server.shutdown()

