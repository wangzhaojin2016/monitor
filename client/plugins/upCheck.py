import commands


def monitor(hostname=None):
    shell_command = "uptime;grep 'processor' /proc/cpuinfo |wc -l"

    status,result = commands.getstatusoutput(shell_command)
    if status != 0:
        value_dic = {'status':status}
    else:
        uptime_result = result
        value_dic = {
            'uptime_result':uptime_result,
            'status':status,
            'hostname':hostname
        }
    return value_dic

if __name__ == "__main__":
    print monitor()