#!/bin/bash
function remove_snap() {
    echo -e "\033[1;31m注意: 执行此操作前，请输入用户密码以确认执行操作!\033[0m"
    sudo echo -e "\033[1m正在一键移除 Snap...\033[0m"
    if [ $? -ne 0 ];then
        exit 1
    fi
    if [ ! -f /usr/bin/snap ];then
        echo "当前未安装 Snap, 无需移除! 3 秒后将关闭..."
        sleep 3s
        exit 0
    fi
    echo -e "\033[1;33m警告: 为确保 Snap 能完全移除，请先关闭 Firefox、Ubuntu Store 等 Snap 应用。\033[0m"
    read -p '若已全部关闭所有 Snap 应用，请按任意键以执行移除操作...' opt 
    echo "(1) 正在移除所有 Snap 软件..."
    if [ -d .cache_snap ];then
        rm -rf .cache_snap
    fi
    sleep 3s
    mkdir .cache_snap
    cd .cache_snap
    touch $(snap list | grep -v Name | cut -d ' ' -f1)
    count=$(ls -1 | wc -l)
    i=1
    for pack in $(ls -r);do
        echo "正在移除 ($i/$count): $pack"
        sudo snap remove $pack &> /dev/null
        i=$(( i+1 ))
    done
    cd ..
    rm -rf .cache_snap
    echo "(2) 正在移除 Snap..."
    sudo apt-get purge snapd -y
    if [ $? -ne 0 ];then
        echo "正在重试..."
        sudo rm -rf /var/lib/dpkg/lock*
        sleep 1s
        sudo apt-get purge snapd -y
    fi
    sudo apt-get autoremove -y
    echo "已完全移除 Snap，3 秒后将自动关闭"
    sleep 3s
    exit 0
}

function install_snap() {
    echo -e "\033[1;31m注意: 执行此操作前，请输入用户密码以确认执行操作!\033[0m"
    sudo echo -e "\033[1m正在一键安装 Snap...\033[0m"
    if [ $? -ne 0 ];then
        exit 1
    fi
    echo "(1) 正在安装 Snap..."
    sudo apt-get install snapd -y
    if [ $? -ne 0 ];then
        echo "Error: 下载安装 Snap 失败!"
        read -p "按任意键以结束执行..."
        exit 1
    fi
    read -p "是否安装 Snap Store 吗? 10 秒后将自动取消安装. (Y/N) " -t 10 opt
    if [[ $opt == 'y' || $opt == 'Y' ]];then
        echo "(2) 正在安装 Snap Store, 这需要较长的时间..."
        sudo snap install snap-store > /dev/null
        if [ $? -ne 0 ];then
            echo "Error: 下载安装 Ubuntu Store 失败!"
            read -p "按任意键以结束执行..."
            exit 1
        fi
    fi
    echo -n "是否额外安装 Firefox Snap 版本吗? 10 秒后将自动取消安装. "
    read -p '(Y/N)' -t 10 opt
    if [[ $opt == 'y' || $opt == 'Y' ]];then
        echo "(3) 正在安装 Firefox Snap 版本..."
        sudo snap install firefox > /dev/null
        if [ $? -ne 0 ];then
            echo "Error: 下载安装 Firefox Snap 版本失败!"
            read -p "按任意键以结束执行..."
            exit 1
        fi
    fi
    echo "完成，即将关闭..."
    sleep 3s
    exit 0
}


echo "你需要对 Snap 作出什么操作？"
echo "输入数字以确认"
select option in 安装 移除; do
    case $option in
        安装)
            # echo "安装"
            install_snap
            ;;
        移除)
            # echo "移除"
            remove_snap
            ;;
    esac
done
