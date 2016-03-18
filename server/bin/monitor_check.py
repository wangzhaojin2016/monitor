import get_path
from plugins import *
class MonitorBase(object):
    """docstring for ClassName"""
    def __init__(self):
        self.plugin = None

class upCheckMonitor(MonitorBase):
    """docstring for ClassName"""
    def __init__(self):
        self.plugin = upCheck

class memoryMonitor(MonitorBase):
    def __init__(self):
        self.plugin = memory

class cpuMonitor(MonitorBase):
    def __init__(self):
        self.plugin = cpu

class diskMonitor(MonitorBase):
    def __init__(self):
        self.plugin  = disk
class processingMonitor(MonitorBase):
    def __init__(self):
        self.plugin  = processing

MonitorListCheck = {
        'upCheck':upCheckMonitor(),
        'memory':memoryMonitor(),
        'cpu':cpuMonitor(),
        'disk':diskMonitor(),
        'processing':processingMonitor()
}
