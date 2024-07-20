import gi  
gi.require_version('Gtk', '3.0')  
from gi.repository import Gtk 
import sys, subprocess, os

class AppWindow(Gtk.ApplicationWindow):  
  
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        self.set_title("快捷工具箱")  
        self.set_default_size(400, 180)  
  
        # 创建笔记本  
        self.notebook = Gtk.Notebook()  
        self.add(self.notebook)  
  
        # 浏览器相关页面  
        browser_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)  
        chrome_button = Gtk.Button(label="Google Chrome")  
        chrome_button.connect("clicked", self.chromium, "google")  
        edge_button = Gtk.Button(label="Microsoft Edge")  
        edge_button.connect("clicked", self.chromium, "edge")
        firefox_button = Gtk.Button(label="Firefox ESR")  
        firefox_button.connect("clicked", self.run_command, f"{appPath}/scripts/firefox_esr.sh")
        browser_box.pack_start(chrome_button, True, True, 0)  
        browser_box.pack_start(edge_button, True, True, 0)  
        browser_box.pack_start(firefox_button, True, True, 0)  
        self.notebook.append_page(browser_box, Gtk.Label(label="浏览器安装"))  
  
        # 输入法相关页面  
        ime_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)  
        fcitx5_button = Gtk.Button(label="Fcitx 5 输入法")  
        fcitx5_button.connect("clicked", self.on_button_clicked, "Fcitx 5 输入法")  
        fcitx4_button = Gtk.Button(label="Fcitx 4 输入法")  
        fcitx4_button.connect("clicked", self.on_button_clicked, "Fcitx 4 输入法")
        ibus_button = Gtk.Button(label="iBus 输入法")  
        ibus_button.connect("clicked", self.on_button_clicked, "iBus 输入法")  
        ime_box.pack_start(ibus_button, True, True, 0)  
        ime_box.pack_start(fcitx5_button, True, True, 0)  
        ime_box.pack_start(fcitx4_button, True, True, 0)  
        self.notebook.append_page(ime_box, Gtk.Label(label="输入法安装"))  
  
        # 杂项页面  
        misc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)  
        snap_button = Gtk.Button(label="一键安装/移除 Snap 商店")  
        snap_button.connect("clicked", self.run_command, f"{appPath}/scripts/Snap.sh")  
        tweaks_button = Gtk.Button(label="快速安装 Gnome Tweaks")  
        tweaks_button.connect("clicked", self.run_command, f"{appPath}/scripts/Install_for_apt.sh gnome-tweaks")  
        extensions_button = Gtk.Button(label="快速安装 Gnome 扩展管理器")  
        extensions_button.connect("clicked", self.run_command, f"{appPath}/scripts/Install_for_apt.sh gnome-shell-extension-manager")  
        misc_box.pack_start(snap_button, True, True, 0)  
        misc_box.pack_start(tweaks_button, True, True, 0)  
        misc_box.pack_start(extensions_button, True, True, 0)  
        self.notebook.append_page(misc_box, Gtk.Label(label="Gnome 通用项")) 

        # 更多页面
        more_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)  
        help_button = Gtk.Button(label="打开 README")  
        help_button.connect("clicked", self.on_button_clicked, "打开 README")  
        more_box.pack_start(help_button, True, True, 0) 
        version_button = Gtk.Button(label="显示版本号")  
        version_button.connect("clicked", self.show_info_dialog, "版本: 0.1.0\n使用 Bash Shell 编写脚本\n使用 GTK 3+ 框架设计 UI")  
        more_box.pack_start(version_button, True, True, 0) 
        github_button = Gtk.Button(label="Github 仓库")  
        github_button.connect("clicked", self.show_question_dialog, "是否使用浏览器访问 Github 仓库？")  
        more_box.pack_start(github_button, True, True, 0)  
        self.notebook.append_page(more_box, Gtk.Label(label="更多"))
  
    def on_button_clicked(self, widget, button_text):  
        print(f"正在执行：{button_text}")  
    
    # 浏览器相关
    def chromium(self, widget, op):
        if op == "google":
            err = self.open_terminal(terminal=terminal, operation=f'{appPath}/scripts/browser.sh Google_Chrome google-chrome-stable https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb')
        elif op == "edge":
            err = self.open_terminal(terminal=terminal, operation=f'{appPath}/scripts/browser.sh Microsoft_Edge microsoft-edge-stable https://packages.microsoft.com/repos/edge/pool/main/m/microsoft-edge-stable/microsoft-edge-stable_126.0.2592.102-1_amd64.deb?brand=M102')
        if err == 128:
            self.show_error_dialog(button_text="错误：找不到打开的终端！")

    # 执行程序
    def run_command(self, widget, command):
        err = self.open_terminal(terminal, command)
        if err == 128:
            self.show_error_dialog(button_text="错误：找不到打开的终端！")

    # 打开后台终端并执行脚本
    def open_terminal(self, terminal, operation):
        command = f'{appPath}/scripts/start_script.sh {terminal} {operation}'
        print(f'正在执行：{command}')
        process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        return process.returncode
    
    # 显示问题对话框
    def show_question_dialog(self, widget, button_text):
        question_dialog = Gtk.MessageDialog(self,  
                                            0,  
                                            Gtk.MessageType.QUESTION,  
                                            Gtk.ButtonsType.YES_NO,  
                                            button_text)  
        response = question_dialog.run()  
        if response == Gtk.ResponseType.YES:  
            question_dialog.destroy()
            return 1  
        elif response == Gtk.ResponseType.NO:  
            question_dialog.destroy()
            return 0 
         
    # 显示错误对话框
    def show_error_dialog(self, button_text):
        error_dialog = Gtk.MessageDialog(self,  
                                         0,  
                                         Gtk.MessageType.ERROR,  
                                         Gtk.ButtonsType.OK,  
                                         button_text)
        error_dialog.run()  
        error_dialog.destroy()  
    
    # 显示警告对话框
    def show_warning_dialog(self, widget, button_text):
        warning_dialog = Gtk.MessageDialog(self,  
                                         0,  
                                         Gtk.MessageType.WARNING,  
                                         Gtk.ButtonsType.OK,  
                                         button_text)
        warning_dialog.run()  
        warning_dialog.destroy() 
    
    # 显示信息对话框
    def show_info_dialog(self, widget, button_text):
        info_dialog = Gtk.MessageDialog(self,  
                                        0,  
                                        Gtk.MessageType.INFO,  
                                        Gtk.ButtonsType.OK,  
                                        button_text)  
        info_dialog.run()  
        info_dialog.destroy()
  
class Application(Gtk.Application):  
  
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, application_id="org.example.SoftwareManager",  
                         **kwargs)  
  
    def do_activate(self):  
        win = AppWindow(application=self)  
        win.show_all()  
        win.present()

def options():
    import configparser
    config = configparser.ConfigParser()
    config.read('config.ini')
    global terminal
    global appPath
    if os.path.exists("config.ini"):
        terminal = config.get('Config', 'terminal')
        appPath = config.get('Config', 'appPath')
    else:
        # run_subprocess("sudo chmod -R u+x ./scripts/*.sh")
        appPath = get_output("pwd")
        terminal = get_output(f"{appPath}/scripts/get_terminal.sh")
        
        context = f'''# 自动生成配置文件
[Config]
appPath={appPath}
terminal={terminal}
# EOF
'''
        with open("config.ini", 'w', encoding='utf-8') as file:
            file.write(context)
        file.close()

def get_output(command):
    process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.stdout.readline().decode('utf-8')
    process.wait()
    return output.strip()

if __name__ == "__main__":  
    options()
    app = Application()  
    exit_status = app.run(sys.argv)  
    sys.exit(exit_status)
