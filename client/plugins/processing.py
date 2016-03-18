#coding=utf8
import re
import commands
from conf.config import processInfo

def monitor_map(port=None):
    port = int(port)
    if port is not None:
        status,result = commands.getstatusoutput("netstat -ntl|grep {0}".format(port))
        if len(result) == 0:
            FailedPort=port
        else:
            FailedPort='OK'

        return FailedPort

    else:
        pass


def monitor(hostname=None):
    value_dic = {'hostname':hostname}

    if  re.search(r'datanode',hostname):
        hostname = 'tt-datanode'
    elif re.search(r'namenode',hostname):
        hostname = 'tt-namenode'
    else:
        pass

    #monitor_dic = processInfo[hostname]
    if processInfo.has_key(hostname):monitor_dic = processInfo[hostname]
    else:return value_dic

    for monitor_name,monitor_port in monitor_dic.iteritems():
        value_dic[monitor_name] = map(monitor_map,monitor_port)

    return value_dic

if __name__ == '__main__':
    print monitor()
