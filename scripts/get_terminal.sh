#!/bin/bash
if [ -f /usr/bin/gnome-terminal ];then
    echo -n "gnome"
elif [ -f /usr/bin/konsole ];then
    echo -n "plasma"
elif [ -f /usr/bin/xfce4-terminal ];then
    echo -n "xfce4"
elif [ -f /usr/bin/qterminal ];then
    echo -n "qt"
fi
