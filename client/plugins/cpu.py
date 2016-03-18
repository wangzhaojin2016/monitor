import commands

#get cpu info
def monitor(hostname=None):
    shell_command = 'sar 1 3 | grep "^Average:"'
    status,result = commands.getstatusoutput(shell_command)
    if status != 0:
        value_dic = {'status':status}
    else:
        user,nice,system,iowait,steal,idle = result.split()[2:]
        value_dic = {
            'user':user,
            'nice':nice,
            'system':system,
            'iowait':iowait,
            'steal':steal,
            'idle':idle,
            'status':status,
            'hostname':hostname
        }
    return value_dic

if __name__ == '__main__':
    print monitor()