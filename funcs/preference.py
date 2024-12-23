# 显示首选项

import gi, configparser
gi.require_version('Gtk', '3.0')  
from gi.repository import Gtk  
  
class Preference(Gtk.Window):  
    def __init__(self):  
        super(Preference, self).__init__(title="首选项")  
        self.set_default_size(300, 150)
        self.set_resizable(False)
  
        # 创建“软体位置”标签和输入框
        self.label_software_location = Gtk.Label(label="定义位置")  
        self.entry_software_location = Gtk.Entry(text=appPath)
        self.entry_software_location.connect("changed", self.on_entry_software_changed) 
  
        # 创建“选择终端”按钮  
        self.label_select_terminal = Gtk.Label(label="选择终端")  
        self.terminal_combo = Gtk.ComboBoxText()  
        terminals = ["Gnome Terminal", "Konsole", "Xfce4 Terminal", "Cosmic", "QTerminal", "Other"]  
        for t_name in terminals:  
            self.terminal_combo.append_text(f"{t_name}")
        if terminal == 'gnome': 
            n = 0
        elif terminal == 'plasma': 
            n = 1
        elif terminal == 'xfce4': 
            n = 2
        elif terminal == 'cosmic':
            n = 3
        elif terminal == 'qt': 
            n = 4
        else: 
            n = 5
        self.terminal_combo.set_active(n)  # 设置默认选项  
        self.terminal_combo.connect("changed", self.on_terminal_combo_changed) 

        # 创建"打开浏览器方式"选项
        self.label_select_browser = Gtk.Label(label="浏览方式")  
        self.browser_combo = Gtk.ComboBoxText()  
        browsers = ["Firefox 全版本", "Chrome/Edge", "Chromium", "<unknown>"]  
        for t_name in browsers:  
            self.browser_combo.append_text(f"{t_name}")
        if browser == 'firefox': 
            n = 0
        elif browser == 'www': 
            n = 1
        else:
            n = 2
        self.browser_combo.set_active(n)  # 设置默认选项  
        self.browser_combo.connect("changed", self.on_browser_combo_changed) 

        # 创建“保存设置”按钮  
        self.button_save_settings = Gtk.Button(label="保存设置")  
        self.button_save_settings.connect("clicked", self.on_save_settings)  
  
        # 创建“取消”按钮（虽然图片中没有显示，但通常会有）  
        self.button_cancel = Gtk.Button(label="取消设置")  
        self.button_cancel.connect("clicked", self.on_cancel)  
        
        # 创建布局容器  
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)  
        # 将组件添加到布局容器中  
        # self.vbox.pack_start(self.label_software_location, False, False, 0)  
        # self.vbox.pack_start(self.entry_software_location, False, False, 0)  
        # self.vbox.pack_start(self.label_select_terminal, False, False, 0)
        # self.vbox.pack_start(self.terminal_combo, False, False, 0)

        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.hbox.pack_end(self.button_save_settings, False, False, 8)
        self.hbox.pack_end(self.button_cancel, False, False, 5)
        # self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        # self.hbox1.pack_start(self.label_software_location, False, False, 10)
        # self.hbox1.pack_start(self.entry_software_location, False, False, 5)
        self.hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.hbox2.pack_start(self.label_select_terminal, False, False, 10)
        self.hbox2.pack_start(self.terminal_combo, False, False, 5)
        self.hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.hbox3.pack_start(self.label_select_browser, False, False, 10)
        self.hbox3.pack_start(self.browser_combo, False, False, 5)

        # self.vbox.pack_start(self.hbox1, False, False, 5)
        self.vbox.pack_start(self.hbox2, False, False, 5)
        self.vbox.pack_start(self.hbox3, False, False, 5)
        self.vbox.pack_end(self.hbox, False, False, 10)
  
        # 将布局容器添加到窗口中  
        self.add(self.vbox)  
  
        # 显示所有组件  
        self.show_all()  
    
    def on_entry_software_changed(self, widget):
        appPath = widget.get_text()
        config.set("Config", "appPath", appPath)

    def on_terminal_combo_changed(self, widget):   
        active = widget.get_active()  
        selected_terminal = widget.get_active_text()  
        if selected_terminal == "Gnome Terminal":
            terminal = 'gnome'
        elif selected_terminal == "Konsole":
            terminal = 'plasma'
        elif selected_terminal == "Xfce4 Terminal":
            terminal = 'xfce4'
        elif selected_terminal == "Cosmic":
            terminal = 'cosmic'
        elif selected_terminal == "QTerminal":
            terminal = 'qt'
        else:
            terminal = 'other'
        config.set('Config', 'terminal', terminal)
    
    def on_browser_combo_changed(self, widget):
        active = widget.get_active()  
        selected_browser = widget.get_active_text()  
        if selected_browser == "Firefox 全版本":
            browser = 'firefox'
        elif selected_browser == "Chrome/Edge":
            browser = 'www'
        elif selected_browser == "Chromium":
            browser = 'chromium'
        else:
            browser = 'unknown'
        config.set('Config', 'browser', browser)

    def on_save_settings(self, widget):  
        # 保存设置的代码将在这里实现  
        with open(conf_file, 'w', encoding='utf-8') as configFile:
            config.write(configFile)
        self.destroy()
  
    def on_cancel(self, widget):  
        # 取消操作的代码将在这里实现  
        self.destroy()
    
def load_config(config_path):
    global conf_file
    conf_file = config_path
    global config
    config = configparser.ConfigParser()
    global terminal
    global browser
    global appPath
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            f.close()
        config.read(config_path)
        terminal = config.get('Config', 'terminal')
        browser = config.get('Config', 'browser')
        appPath = config.get('Config', 'appPath')
        return config
    except FileNotFoundError as e:
        print("Error: 未初始化配置! 无法获取配置信息!")
        return None
        

def main(setup_path):
    return_conf = load_config(setup_path)
    if return_conf == None:
        return 127
    win = Preference()  
    win.connect("destroy", Gtk.main_quit)  # 当窗口关闭时退出主循环  
    Gtk.main()
    return return_conf
  
