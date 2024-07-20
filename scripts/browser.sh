#!/bin/bash

if [ $# -ne 3 ];then
    exit 0
fi

# 获取
APP_NAME=$1
PACK_NAME=$2
URL=$3

echo -e "开始下载安装 \033[1m$APP_NAME\033[0m..."
echo -e "\033[1;31m注意: 执行前, 请先输入用户密码以继续执行后续操作!\033[0m"
sudo echo -e "\033[1m: 已提权 :\033[0m"
if [ $? -ne 0 ];then
    exit 1
fi
sleep 1s

# 检查软件包更新
echo "(1) 正在检查更新..."
sudo apt install $PACK_NAME
if [ $? -eq 0 ];then
    echo "已安装 $APP_NAME, 3 秒后将自动关闭."
    sleep 3s
    exit 0
fi

# 清理缓存
function clean_package() {
    cd ..
    rm -rf .cache_pack
}

# 从指定网页中下载软件包
echo "(2) 下载软件包..."
if [ -d .cache_pack ];then
    rm -rf .cache_pack
fi
mkdir .cache_pack
cd .cache_pack
wget $URL

if [ $? -ne 0 ];then
    echo "Error: 下载软件包时出现错误！"
    read -p "按任意键以结束执行..."
    clean_package
    exit 1
fi

# 安装软件包
echo "(3) 安装软件包..."
sudo dpkg -i $(ls)

if [ $? -ne 0 ];then
    echo "Error: 安装软件包时出现错误！"
    read -p "按任意键以结束执行..."
    clean_package
    exit 1
fi
echo "已安装 $APP_NAME, 3 秒后将自动关闭."
sleep 3s