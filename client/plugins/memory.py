import commands

def monitor(hostname=None):
    monitor_dic = {
    'SwapUsage':'percentage',
    'MemUsage':'percentage'
    }

    shell_command = 'grep "MemTotal\|MemFree\|Buffers\|^Cached\|SwapTotal\|SwapFree" /proc/meminfo'

    status,result = commands.getstatusoutput(shell_command)
    if status != 0:
        value_dic = {'status':status}
    else:
        value_dic = {'status':status}
        for i in result.split('kB\n'):
            key = i.split(':')[0]
            value = i.split()[1]
            value_dic[key] = value
        if monitor_dic['SwapUsage'] == 'percentage':
            value_dic['SwapUsage_P'] = 100 - int(value_dic['SwapFree']) * 100 / int(value_dic['SwapTotal'])
        value_dic['SwapUsage'] = int(value_dic['SwapTotal']) - int(value_dic['SwapFree'])
        
        """used memory"""
        MemUsage = int(value_dic['MemTotal']) - (int(value_dic['MemFree']) + \
            int(value_dic['Buffers']) + int(value_dic['Cached']))

        if monitor_dic['MemUsage'] == 'percentage':
            value_dic['MemUsage_p'] = int(MemUsage) * 100 / int(value_dic['MemTotal'])
        value_dic['MemUsage']  = MemUsage
        value_dic['hostname']  = hostname
    return value_dic

if __name__ == '__main__':
    print monitor()
