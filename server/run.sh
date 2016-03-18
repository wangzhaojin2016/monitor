#!/bin/bash
#!/bin/bash

ctrl=$1

if [ "$#" -ne "1" ];then
    echo "Scripts need parameters,parameters=1"
    echo "For example:"
    echo "sh run start|stop|check" 
    exit 1
fi
pid=$(ps -ef|grep 'monitor_server'|grep -v grep | awk '{print $2}')
pingpid=$(ps -ef|grep 'pingLive'|grep -v grep | awk '{print $2}')
function __start_monitor_server(){
    [ "$pid" != "" ] && echo "python monitor_server process is exitst,pid is $pid" && exit 1
    cd log
    [ -f console.log.bak ] && rm -f console.log.bak
    [ -f console.log ] && mv console.log console.log.bak
    cd -
    nohup python -u bin/monitor_server.py >log/console.log 2>&1 &
}

function __start_pingLive(){
    [ "$pingpid" != "" ] && echo "python pingLive process is exitst,pid is $pid" && exit 1
    nohup python -u bin/pingLive.py >log/ping.log 2>&1 &
}

function __stop(){
    kill $pid 
    kill $pingpid
    echo "kill python complate"
}

function __check(){
    pid=$(ps -ef|grep 'monitor_server'|grep -v grep | awk '{print $2}')
    pingpid=$(ps -ef|grep 'pingLive'|grep -v grep | awk '{print $2}')
    if [[ "${pid}" != "" ]];then
        echo "monitor_server is running,pid is $pid"
    else
        echo "monitor_server is stoped"
    fi
    if [[ "${pingpid}" != "" ]];then
        echo "pingLive is running,pid is $pingpid"
    else
        echo "pingLive is stoped"
    fi
    exit 1
}

case "$ctrl" in
start)
    __start_monitor_server
    __start_pingLive
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
