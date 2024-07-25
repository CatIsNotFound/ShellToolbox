#!/bin/bash
# iBus 输入法安装与卸载

# 快速配置
set_ibus(){
    if [ -f /usr/bin/gnome-control-center ];then
        echo "正在跳转至 Gnome 设置..."
        sleep 1s
        gnome-control-center region
    else
        echo "正在跳转至 ibus 首选项..."
        sleep 1s
        ibus-setup
    fi
}

# 测试
test_ibus() {
    echo -e "\033[33m提示: 为了确认您已正确配置输入法，请直接尝试按下 \033[1mMeta(Win) + 空格键\033[0m\033[33m以尝试切换输入法. \033[0m"
    echo -e "\033[1;31m注意: 部分终端软件下可能无法直接输入中文, 请尝试打开任意文本编辑器以测试输入. \033[0m"
    read -p "若能够正常输入中文，请输入【yes】并按下回车键结束测试, 否则请直接按下回车键. (yes) " OPT
    if [[ $OPT == 'yes' ]];then
        exit 0
    fi
    read -p "是否尝试配置 ibus? (y/n) " opt
    if [[ $opt == 'y' || $opt == 'Y' ]];then
        set_ibus
    fi
    read -p "是否尝试重启 ibus? (y/n) " opt
    if [[ $opt == 'y' || $opt == 'Y' ]];then
        repair_ibus
    fi
    read -p "是否尝试写入 ibus 环境? (y/n) " opt
    if [[ $opt == 'y' || $opt == 'Y' ]];then
        repair_ibus env
    fi
}

# 安装
install_ibus() {
    echo -e "\033[1;31m注意: 请输入用户密码以确认执行操作!\033[0m"
    sudo echo -e "\033[1m:已提权:\033[0m"
    if [ $? -ne 0 ];then
        exit 1
    fi
    echo "正在下载并安装 iBus..."
    sudo apt-get install ibus ibus-pinyin ibus-sunpinyin ibus-libpinyin -y > /dev/null
    if [ $? -ne 0 ];then
        echo "Error: 下载时出现错误! "
        read -p "按任意键以结束执行..."
        exit 1
    fi
    echo "正在启动 ibus..."
    ibus exit
    sleep 1s
    ibus-daemon -d -R
    if [ $? -ne 0 ];then
        echo "Error: 启动时出现错误! "
        read -p "按任意键以结束执行..."
        exit 1
    fi
    sleep 1s
    read -p "ibus 已安装完成, 是否立刻配置? 10 秒后将自动结束. (yes / no) " -t 10 opt
    if [[ $opt == 'yes' ]];then
        set_ibus
        while $1 ; do
            test_ibus
        done
    fi
    
}

# 更新
update_ibus() {
    echo -e "\033[1;31m注意: 请输入用户密码以确认执行操作!\033[0m"
    sudo echo -e "\033[1m:已提权:\033[0m"
    if [ $? -ne 0 ];then
        exit 1
    fi
    echo "正在更新 ibus..."
    list=$(apt list --installed ibus* 2> /dev/null | grep '/' | cut -d '/' -f1)
    sudo apt-get install $list -y
    if [ $? -ne 0 ];then
        echo "Error: 更新时出现错误! "
        read -p "按任意键以结束执行..."
        exit 1
    fi
    exit 0
}

# 移除
remove_ibus() {
    echo -e "\033[1m正在准备移除 ibus...\033[0m"
    echo -e "\033[1;31m注意: 请输入用户密码以确认执行操作!\033[0m"
    sudo echo -e "\033[1m:已提权:\033[0m"
    if [ $? -ne 0 ];then
        exit 1
    fi
    echo "正在关闭 ibus..."
    ibus exit
    sleep 1s
    echo "" > ~/.bash_profile
    echo "正在移除 ibus..."
    sudo apt-get purge ibus -y > /dev/null
    sudo apt-get autoremove -y > /dev/null
    echo "已完全移除 ibus, 3 秒后将自动关闭"
    sleep 3s
    exit 0
}

repair_ibus() {
    if [[ $1 == 'env' ]];then
        echo "正在写入环境变量..."
        cat > $HOME/.bash_profile << EOF
# Auto-generated by scripts.
export GTK_IM_MODULE=ibus
export XMODIFIERS=ibus
export QT_IM_MODULE=ibus
EOF
        sleep 1s
        echo -e "\033[33m注意: 请按下 \033[1mCtrl + Alt + Delete\033[0m\033[33m 以注销当前用户并重新登录以生效配置.\033[0m "
        read -p "请按任意键以结束..."
        exit 0
    fi
    echo "正在重新启动 iBus..."
    ibus-daemon -R -d
    if [ $? -ne 0 ];then
        echo -e "\033[1;31mError: 无法启动 iBus 输入法!\033[0m"
        read -p "请按任意键以结束..."
        exit 1
    fi
    echo -e "\033[0;32m提示：请尝试在当前会话下按下 Meta(Windows) + 空格键以尝试切换输入法...\033[0m"
    read -p "若已正常显示，请输入 '否' 结束测试，否则请直接按回车键以继续... (否) " OPT
    if [[ $OPT == '否' ]];then
        exit 0
    fi
}

check_fcitx() {
    if [ -f /usr/bin/fcitx ];then
        T=fcitx
    elif [ -f /usr/bin/fcitx5 ];then
        T=fcitx5
    fi
    if [ $T ];then
        echo "检查到当前系统下已安装 $T, 是否确认移除并安装 ibus? "
        echo -e "\033[1m注意：ibus 不能与 fcitx 一同安装! \033[0m"
        read -p "是否移除 fcitx? (yes) " OPT
        if [[ $OPT == 'yes' ]];then
            echo -e "\033[1m正在准备移除...\033[0m"
            echo -e "\033[1;31m注意: 请输入用户密码以确认执行操作!\033[0m"
            sudo echo -e "\033[1m:已提权:\033[0m"
            if [ $? -ne 0 ];then
                exit 1
            fi
            echo "" > ~/.bash_profile
            echo "正在移除 $T 及其组件..."
            sudo apt-get purge $T -y > /dev/null
            while [ $? -ne 0 ]; do
                sudo rm -rf /var/lib/dpkg/lock*
                sleep 2s
                sudo apt-get purge $T -y > /dev/null
            done
            sudo apt-get autoremove -y > /dev/null
            return 0
        else
            exit 1
        fi
    fi
    return 0
}

if [ -f /usr/bin/ibus ];then
    echo -e "需要对 iBus 输入法做什么？"
    select option in 安装拼音 更新 移除 配置 测试 重新启动 退出; do
        case $option in
            安装拼音)
                install_ibus
                ;;
            更新)
                update_ibus
                ;;
            移除)
                remove_ibus
                ;;
            配置)
                set_ibus
                ;;
            测试)
                while $1; do
                    test_ibus
                done
                ;;
            重新启动)
                repair_ibus
                ;;
            退出)
                exit 0
                ;;
        esac
    done
else
    check_fcitx
    echo -e "\033[1m准备下载安装 ibus...\033[0m"
    install_ibus
fi