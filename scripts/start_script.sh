#!/bin/bash
# 查看使用的终端
case $1 in
    gnome)
        gnome-terminal -- $2 $3 $4 $5 $6 $7 $8 $9
        ;;
    plasma)
        konsole -e $2 $3 $4 $5 $6 $7 $8 $9
        ;;
    xfce4)
        xfce4-terminal -e $2 $3 $4 $5 $6 $7 $8 $9
        ;;
    qt)
        qterminal -e $2 $3 $4 $5 $6 $7 $8 $9
        ;;
    *)
        # echo "错误：找不到终端以执行！"
        echo -n "127"
        exit 127
        ;;
esac
if [ $? -ne 0 ];then
    echo -n "128"
    exit 128
fi