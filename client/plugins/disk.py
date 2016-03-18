import commands
import sys

def monitor(hostname=None):

    shell_command = 'df -h | egrep "(/$|/data$|^Filesystem)"'
    status,result = commands.getstatusoutput(shell_command)
    if status != 0:
        value_dic = {'status':status}
    else:
        value_dic = {'status':status,'hostname':hostname}
        list_result = result.split('\n')
        for i in list_result:
            if i.split()[0] == 'Filesystem':
                value_dic['Filesystem'] = i.split()
            else:
                value_dic[i.split()[-1]] = repr(i).split()

    return value_dic

if __name__ == "__main__":
    print monitor()
