#!/bin/bash
# 在 GNOME 环境下修改窗口标题栏按钮布局

if [ ! -f /usr/bin/gsettings ];then
    echo -e "\033[1;31m错误: 此脚本仅支持为 GTK2/3+ 窗口设置. \033[0m"
    read -p "按任意键结束执行..."
    exit 1
fi

echo "需要为 GTK2/GTK3+ 窗口的标题栏设置什么按钮布局风格？"
echo "示例:  ✕ _ ◻ (Mac);  _ ◻ ✕ (Windows)"
echo "输入数字以确认, 按 Ctrl+D 结束执行..."
select option in mac windows; do
    case $option in
        mac)
            gsettings set org.gnome.desktop.wm.preferences button-layout "close,minimize,maximize:"
            echo "已设置..."
            ;;
        windows)
            # echo "移除"
            gsettings set org.gnome.desktop.wm.preferences button-layout ":minimize,maximize,close"
            echo "已设置..."
            ;;
    esac
done

# _ ◻ ✕