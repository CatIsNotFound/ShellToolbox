#!/bin/bash
# 设置熄屏时长
echo "此脚本用于设置熄屏延时时长，若需禁用请直接选择第 (1) 项以禁用熄屏。"
echo "请输入数字键以设置分钟数..."
select option in 禁用 1 2 3 4 5 8 10 15; do
    case $option in
        禁用)
            gsettings set org.gnome.desktop.session idle-delay 0
            echo "已禁用熄屏..."
            ;;
        *)
            gsettings set org.gnome.desktop.session idle-delay $((60 * ${option}))
            echo "已设置 $option 分钟后熄屏..."
            ;;
    esac
done