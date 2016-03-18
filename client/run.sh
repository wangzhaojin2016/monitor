#!/bin/bash
#!/bin/bash

ctrl=$1

if [ "$#" -ne "1" ];then
    echo "Scripts need parameters,parameters=1"
    echo "For example:"
    echo "sh run start|stop|check" 
    exit 1
fi
pid=$(ps -ef|grep 'client_monitor'|grep -v grep | awk '{print $2}')
function __start(){
    cd log/
    [ "$pid" != "" ] && echo "python process is exitst,pid is $pid" && exit 1
    [ -f console.log.bak ] && rm -f console.log.bak
    [ -f console.log ] && mv console.log console.log.bak
    cd -
    nohup python -u bin/client_monitor.py >log/console.log 2>&1 &
    exit
}

function __stop(){
    killall python 
    echo "kill python complate"
}

function __check(){
    pid=$(ps -ef|grep 'client_monitor'|grep -v grep | awk '{print $2}')
    if [[ "${pid}" != "" ]];then
        echo "client_monitor is running,pid is $pid"
    else
        echo "client_monitor is stoped"
    fi
    exit 1
}

case "$ctrl" in
start)
__start
;;
stop)
__stop
;;
check)
__check
;;
*)
printf "$num Arguments are error!You only set: start|check|stop"
;;
esac
