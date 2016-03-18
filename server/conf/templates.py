from  services  import Linux

class BaseTemplate(object):
    name = None
    groups = []
    hosts = []
    service_dic = {} 

class LinuxGemericServices(BaseTemplate):
    name = 'Linux Generic services'
    groups = ['BJ']
    hosts = []
    service_dic = {
        'cpu':Linux.cpu(),
        'memory':Linux.memory(),
        'upCheck':Linux.upCheck()
    }

class WindowsGemericServices(BaseTemplate):
    name = 'Linux Generic services'
    groups = ['BJ']
    hosts = []
    service_dic = {
        'cpu':Linux.cpu(),
        'memory':Linux.memory(),
        'upCheck':Linux.upCheck()
    }

enabled_templates = (
    LinuxGemericServices(),
    WindowsGemericServices(),
)