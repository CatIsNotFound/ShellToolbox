#!/bin/bash

if [ -f /usr/bin/firefox ];then
    echo -n "firefox"
elif [ -f /usr/bin/gnome-www-browser ];then
    echo -n "www"
else
    echo -n "unknown"
fi