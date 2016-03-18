class DefaultService:
    def __init__(self):
        self.name = None
        self.interval = 30
        self.warning_retry = 3
        self.critical_retry = 1
        self.data_from = 'agent'
        self.lt_operator = []   #if this sets to empty,all the status will be caculated in > mode,gt = >   ,less thran

class upCheck(DefaultService):
    def __init__(self):
        self.name = 'uptime'
        self.level_dic = {
            'uptime_Level':['level_Value',5,8]
        }

class memory(DefaultService):
    def __init__(self):
        self.name = 'memory'
        self.level_dic = {
            'MemUsage_p':['percentage', 85, 95],
            'SwapUsage_p':['percentage',30, 50]
        }

class cpu(DefaultService):
    def __init__(self):
        self.name = 'cpu'
        self.lt_operator = ['idle']
        self.level_dic = {
            'iowait':['percentage', 80, 90],
            'system':['percentage', 80, 90],
            'idle':['percentage',30, 20]
        }

class disk(DefaultService):
    def __init__(self):
        self.name = 'disk'
        self.level_dic = {'DiskUse':['percentage',96]}

class processing(DefaultService):
    def __init__(self):
        self.name = 'processing'
