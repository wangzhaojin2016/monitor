#coding=utf8

##############基础监控设置##############
MASTER_HOST = '192.168.5.11'
MASTER_PORT = 9999

##############进程监控设置##############
#                                      #
#   通过hostname来设置监控端口         #
#                                      #
########################################
processInfo={
    'tt-datanode':{
        'datanode':[50010,50075,50020],
	'nodemanager':[13562,8040]
     },
    'tt-namenode':{
        'zookeeper':[2181,3888],
        'namenode':[50070,9000],
        'zkfc':[8019],
        'journalnode':[8480,8485]
    },
    'tt-yarn':{
        'zookeeper':[2181,3888],
        'journalnode':[8480,8485],
        'resourcemanager':[8088,8030,8031,8032,8033],
        'hive':[10001]
    }
}
