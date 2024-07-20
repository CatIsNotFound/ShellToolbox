#!/bin/bash
echo -e "开始下载安装 \033[1m$1\033[0m..."
echo -e "\033[1;31m注意: 执行前, 请先输入用户密码以继续执行后续操作!\033[0m"
sudo echo -e "\033[1m: 已提权 :\033[0m"
if [ $? -ne 0 ];then
    exit 1
fi
sleep 1s
sudo apt install $1 -y
