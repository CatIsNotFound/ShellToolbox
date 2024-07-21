#!/bin/bash
# Install Firefox ESR

echo "开始下载安装 Firefox ESR..."
echo -e "\033[1;31m注意: 执行此操作前，请输入用户密码以确认执行操作!\033[0m"
sudo echo ":已提权:"
if [ $? -ne 0 ];then
    exit 1
fi
# 检查是否安装 Firefox Snap 版本
if [ -f /usr/bin/snap ];then
    snap list | grep firefox
    if [ $? -eq 0 ];then
        read -p "检查到你已安装 Firefox Snap 版本，确认将其移除? (Y/N)" opt
        if [[ $opt == 'y' || $opt == 'Y' ]];then
            echo "正在移除 Firefox, 这需要一点时间..."
            sudo snap remove firefox > /dev/null
        else
            echo "正在取消安装 Firefox ESR..."
            sleep 3s
            exit 0
        fi
    fi
fi

# 检查 apt 是否已存在 firefox
echo "正在检查..."
sudo apt-get update > /dev/null
if [ $? -ne 0 ];then
    echo "Error: 获取失败, 请检查网络!"
    read -p "按任意键以结束执行..."
fi
if [ $(apt list firefox --installed 2> /dev/null | wc -l) -gt 1 ];then
    echo -e "\033[33m警告: 检测到当前系统上已安装 Firefox, 但这可能是\033[1m旧版本的 Firefox\033[0m"
    read -p "是否确认移除 Firefox 并安装 Firefox ESR 版本? (y/n) " opt
    if [[ $opt == 'y' || $opt == 'Y' ]];then
        echo "正在移除 Firefox..."
        sudo apt-get purge firefox -y
    fi
fi
if [ $(apt list firefox-esr* --installed 2> /dev/null | wc -l) -ge 2 ];then
    echo "检测到您已安装 Firefox ESR 版本, 你希望选择卸载还是更新? "
    read -p "输入 [remove] 以确认卸载, 或按任意键以检查更新. (remove) " opt
    if [[ $opt == 'remove' ]];then
        echo "正在移除 Firefox ESR..."
        sudo apt-get purge firefox-esr -y &> /dev/null
        echo "已移除 Firefox ESR, 即将结束执行..."
        sleep 3s
        exit 0
    fi
fi

if [ $(apt search firefox-esr --names-only 2> /dev/null | wc -l) -gt 2 ];then
    echo "正在下载更新 Firefox ESR..."
    sudo apt-get install firefox-esr firefox-esr-l10n-zh-cn -y &> /dev/null
    if [ $? -eq 0 ];then
        echo "已安装更新 Firefox ESR, 即将结束执行..."
        sleep 3s
        exit 0
    fi
fi

# 下载 Firefox ESR 版本
echo "(1) 正在获取并添加密钥..."
sudo install -d -m 0755 /etc/apt/keyrings
wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O- | sudo tee /etc/apt/keyrings/packages.mozilla.org.asc > /dev/null
if [ $? -ne 0 ];then
    echo "Error: 获取错误, 请检查网络!"
    read -p "按任意键以结束执行..."
fi
echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] https://packages.mozilla.org/apt mozilla main" | sudo tee -a /etc/apt/sources.list.d/mozilla.list > /dev/null
echo '
Package: *
Pin: origin packages.mozilla.org
Pin-Priority: 1000
' | sudo tee /etc/apt/preferences.d/mozilla
echo "(2) 正在更新软件源..."
sudo apt-get update > /dev/null
if [ $? -ne 0 ];then
    echo "Error: 更新失败, 请检查网络!"
    read -p "按任意键以结束执行..."
fi
echo "(3) 正在下载 Firefox ESR 及简体中文语言包..."
sudo apt-get install firefox-esr firefox-esr-l10n-zh-cn -y > /dev/null
if [ $? -ne 0 ];then
    echo "Error: 下载安装时出现错误!"
    read -p "按任意键以结束执行..."
fi
echo "已安装 Firefox ESR 版本, 即将结束执行..."
sleep 3s
exit 0