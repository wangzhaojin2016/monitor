import sys
from plugins import cpu,disk,memory,upCheck,processing

class MonitorBase(object):
    """docstring for ClassName"""
    def __init__(self):
        self.interval = 300
        self.plugin = None

class upCheckMonitor(MonitorBase):
    """docstring for ClassName"""
    def __init__(self):
        self.interval = 60
        self.plugin = upCheck

class memoryMonitor(MonitorBase):
    def __init__(self):
        self.interval = 120
        self.plugin = memory

class cpuMonitor(MonitorBase):
    def __init__(self):
        self.interval = 120
        self.plugin = cpu

class diskMonitor(MonitorBase):
    def __init__(self):
        self.interval  = 300
        self.plugin    = disk
class processingMonitor(MonitorBase):
    def __init__(self):
        self.interval  = 300
        self.plugin    = processing


enabled_services = {
    'service':{
        'upCheck':upCheckMonitor(),
        'memory':memoryMonitor(),
        'cpu':cpuMonitor(),
        'disk':diskMonitor(),
        'processing':processingMonitor()
        }
}
