#!/bin/bash
# 调整日期时间工具

echo "注：此工具用于已安装双系统（Windows + Debian/Ubuntu）的情况下使用，若出现时间不同步的问题，请直接按下回车键以调整。"
read -p "按下回车键以确认同步时间，或按下 Ctrl+C 取消执行... "

timedatectl set-local-rtc true --adjust-system-clock

echo "日期时间已被调整为如下："
timedatectl
read -p "按任意键以结束执行..."