#!/bin/bash
# Fcitx 4 / Fcitx 5 安装与卸载

function remove_fcitx() {
    echo -e "\033[1m正在准备移除...\033[0m"
    echo -e "\033[1;31m注意: 请输入用户密码以确认执行操作!\033[0m"
    sudo echo -e "\033[1m:已提权:\033[0m"
    if [ $? -ne 0 ];then
        exit 1
    fi
    echo "正在移除 $1..."
    sudo apt-get purge $2 -y
    sudo apt autoremove -y > /dev/null
    echo "已彻底移除 $1, 即将结束执行."
    sleep 3s
    exit 0
}


function select_2_install() {
    
}

if [ -f /usr/bin/fcitx5 ];then
    VAR=fcitx5
    NAME='Fcitx 5'
elif [ -f /usr/bin/fcitx ];then
    VAR=fcitx
    NAME='Fctix 4'
else
    select_2_install
fi


