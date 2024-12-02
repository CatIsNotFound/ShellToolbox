#!/bin/bash
# 用于安装 SSH 服务器

sudo echo -e "\033[1m:已提权:\033[0m"
if [ $? -ne 0 ];then
    echo "Error: 未授权管理员身份执行脚本!"
    read -p "按任意键以结束执行."
    exit 128
fi
sleep 1s
echo "正在检查 SSH 服务..."
if [ -f /etc/ssh/sshd_config ];then
    echo "已安装 SSH 服务."
    echo "正在检查 SSH 服务是否正在运行..."
    sleep 1s
    systemctl is-active sshd > /dev/null
    if [ $? -ne 0 ];then
        echo "正在启动 SSH 服务..."
        sleep 1s
        sudo systemctl start sshd
        if [ $? -ne 0 ];then
            echo "Error: 启动 SSH 服务时出现错误!"
            read -p "按任意键以结束执行."
            exit 1
        fi
    fi
else
    echo "正在安装 SSH 服务..."
    sudo apt-get install openssh-server -y
    if [ $? -ne 0 ];then
        echo "Error: 安装 SSH 服务时出现错误!"
        read -p "按任意键以结束执行."
        exit 1
    fi
fi
echo "已启动 SSH 服务!"
echo "5 秒后将自动退出..."
sleep 5s
