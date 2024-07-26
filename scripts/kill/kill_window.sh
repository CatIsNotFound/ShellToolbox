#!/bin/bash
# 通过鼠标选择窗口获取 PID, 并将其结束/杀死进程

if [[ $XDG_SESSION_TYPE != 'x11' ]];then
    echo -e "\033[1;31mError: 此脚本仅适用于 X11 窗口管理器! \033[0m"
    read -p "请按任意键以结束."
    exit 1
fi
# echo -e "\033[1;32m说明请参见: https://github.com/CatIsNotFound/ShellToolbox/wiki\033[0m "
echo "请将未响应或假死的程序置于前方 (鼠标能够点击到的地方)"
read -p "完成后，请按任意键以开始捕获窗口."
echo -e "\n\033[1;33m请用鼠标点击窗口以直接关闭. \033[0m"
echo "按 Ctrl+C 以取消执行操作."
xprop > .xwininfo
IS_CLOSE=0
while [ $IS_CLOSE -eq 0 ]; do
    WIN_PID=`cat .xwininfo | grep _NET_WM_PID\(CARDINAL\) | cut -d ' ' -f3`
    if [ ! $WIN_PID ];then
        sleep 1s
        WIN_CLASS=`cat .xwininfo | grep WM_CLASS\(STRING\) | cut -d ' ' -f4 | cut -d '"' -f2`
        if [ ! $WIN_CLASS ];then
            echo -e "\033[1;31mError: 捕获失败! 请重新尝试!\033[0m"
            xprop > .xwininfo
        else
            killall $WIN_CLASS
            rm -rf .xwininfo
            exit 0
        fi
    else
        kill $WIN_PID 
        if [ $? -ne 0 ];then
            read -p "错误: 无法直接结束此进程, 是否尝试使用管理员权限强制结束进程? (yes) [默认: no]" OPT
            if [[ $OPT == 'yes' ]];then
                echo -e "\033[1;31m警告: 你正在尝试使用高级权限强行关闭程序, 请谨慎执行.\033[0m"
                sudo kill -9 $WIN_PID
            fi
        fi
        rm -rf .xwininfo
        exit 0
    fi
done



