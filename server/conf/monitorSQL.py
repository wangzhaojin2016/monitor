#
#
# create table info

dbinfo = {
"monitor_hostinfo":"""
CREATE TABLE IF NOT EXISTS `monitor_hostinfo` (
`id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增值id',
`host` varchar(20) NOT NULL COMMENT '主机ip',
PRIMARY KEY (`id`),
UNIQUE KEY `host` (`host`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='监控的IP表';
"""
}
