#!/bin/bash
# 查看使用的终端
case $1 in
    gnome)
        gnome-terminal -- $2 $3 $4 $5 $6 $7 $8 $9
        ;;
    kde)
        konsole -e "bash" $2 $3 $4 $5 $6 $7 $8 $9
        ;;
    xfce4)
        xfce4-terminal -e "bash $2 $3 $4 $5 $6 $7 $8 $9"
        ;;
    qt)
        qterminal -e 'bash' $2 $3 $4 $5 $6 $7 $8 $9
        ;;
    *)
        # echo "错误：找不到终端以执行！"
        exit 128
        ;;
esac
echo $@

if [ $? -ne 0 ];then
    # echo "错误：无法打开终端执行！"
    exit 128
fi