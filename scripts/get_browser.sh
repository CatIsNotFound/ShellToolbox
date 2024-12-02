#!/bin/bash

if [ -f /*/bin/firefox* ];then
    echo -n "firefox"
elif [ -f /usr/bin/gnome-www-browser ];then
    echo -n "www"
elif [ -f /usr/bin/chromium ];then
    echo -n "chromium"
else
    echo -n "unknown"
fi