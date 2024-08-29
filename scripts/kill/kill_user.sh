#!/bin/bash
# （存在风险）杀死指定用户的所有进程，以直接强制注销

echo -e "\033[1;33m警告: 此脚本不建议使用, 请满足以下条件以确认才能执行! \033[0m\n"
echo -e "\033[1m1) 确认保存所有文件并关闭所有重要应用程序"
echo "2) 不能正常地注销（注销没有任何响应）"
echo -e "3) 已通知正在使用此账户的用户以做好保存或备份\033[0m\033[0m\n"

echo -e "\033[1;31m注意: 此脚本执行后可能会影响到所有登录于同一账户的用户, 请谨慎使用! \033[0m\n"

echo "请仔细阅读以上警告."
sleep 3s


LOGIN_USER_NUM=`who | cut -d ' ' -f1 | uniq | wc -l`
if [ $LOGIN_USER_NUM -ge 2 ];then
    echo "请选择用户以确认强制杀死. 若需撤销操作, 请直接 Ctrl+C 结束! "
    select LOGIN_USER in `who | cut -d ' ' -f1 | sort | uniq`; do
        case $LOGIN_USER in
            *)
                echo -e "\033[1;31m注意: 请输入管理员密码以确认!\033[0m\n"
                sudo pkill -9 -u $LOGIN_USER
                exit 0
                ;;
        esac
    done
else
    LOGIN_USER=`who | cut -d ' ' -f1 | uniq`
    echo -e "是否确认强制杀死 \033[1m$LOGIN_USER\033[0m?" 
    read -p "输入 [yes] 以确认 (yes/no) [默认: no] " OPT
    if [[ $OPT == 'yes' ]];then
        echo -e "\033[1;31m注意: 请输入管理员密码以确认!\033[0m\n"
        sudo pkill -9 -u $LOGIN_USER
        exit 0
    fi
fi