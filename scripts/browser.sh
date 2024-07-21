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
echo "(0) 正在检查..."
if [ $(apt list $PACK_NAME --installed 2> /dev/null | wc -l) -gt 1 ];then
    echo "检查到您已安装 $APP_NAME, 是否考虑卸载或更新? "
    read -p "输入 [remove] 以确认卸载, 直接按下回车键以更新软件包. (remove) " opt
    if [[ $opt == 'remove' ]];then
        echo "正在移除 $APP_NAME..."
        sudo apt-get purge $PACK_NAME -y &> /dev/null
        echo "已移除 $APP_NAME, 即将结束执行..."
        sleep 3s
        exit 0
    fi
fi
echo "(1) 正在下载更新..."
sudo apt-get install $PACK_NAME > /dev/null
if [ $? -eq 0 ];then
    echo "已安装 $APP_NAME, 即将结束执行...."
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
flag='1'
while [[ $flag == '1' ]];do
echo "(3) 安装软件包..."
sudo dpkg -i $(ls)
if [ $? -ne 0 ];then
    echo -e "\033[31mError: 安装软件包时出现错误! 这可能有\033[1m进程正在占用或存在依赖问题.\033[0m"
    echo "请选择以下选项: "
    echo "1: 解决依赖"
    echo "2: 强制解除占用并重新安装"
    echo "Enter: 重新安装"
    read -p "选择: " opt
    if [[ $opt == '1' ]];then
        while [[ $flag == '1' ]]; do
            echo "(4) 正在解决依赖中..."
            sudo apt install -f -y > /dev/null
            if [ $? -ne 0 ];then
                echo "Error: 下载依赖时出现问题! "
                read -p "请检查网络连接或结束某一进程的 apt 以继续下载... (按任意键继续) "
            else
                if [ $(apt list $PACK_NAME --installed 2> /dev/null | wc -l) -le 1 ];then
                    echo "Error: 解决依赖失败! 未能成功安装 $APP_NAME!"
                    read -p "请按任意键以结束执行..."
                    clean_package
                    exit 2
                fi
                flag='0'
            fi
        done
    elif [[ $opt == '2' ]];then
        sudo rm -rf /var/lib/dpkg/lock*
        continue
    else
        continue
    fi
    echo "已安装 $APP_NAME, 即将结束执行...."
    sleep 3s
    clean_package
    exit 0
fi
break
done
echo "已安装 $APP_NAME, 即将结束执行...."
clean_package
sleep 3s