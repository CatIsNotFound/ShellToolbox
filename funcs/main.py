from time import sleep
import gi  
gi.require_version('Gtk', '3.0')  
from gi.repository import Gtk 
import sys, subprocess, os, configparser
from funcs import preference, update_gui

class AppWindow(Gtk.ApplicationWindow):  
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        self.set_title("Shell Toolbox")  
        # self.set_default_size(600, 180)
        self.set_resizable(False)  
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)  
        self.add(box)

        # 绘制菜单栏
        menu_bar = Gtk.MenuBar()  
        box.pack_start(menu_bar, False, False, 0)

        # "程序" 菜单栏
        file_menu = Gtk.MenuItem(label="程序")  
        menu_bar.append(file_menu)  
        file_menu_dropdown = Gtk.Menu()  
        file_menu.set_submenu(file_menu_dropdown)  

        # "程序" 菜单项
        config_item = Gtk.MenuItem(label="首选项")  
        config_item.connect("activate", self.on_open_preference)  
        file_menu_dropdown.append(config_item)
        quit_item = Gtk.MenuItem(label="退出")  
        quit_item.connect("activate", self.on_quit)  
        file_menu_dropdown.append(quit_item) 

        # # "工具" 菜单栏
        # tools_menu = Gtk.MenuItem(label="额外工具")  
        # menu_bar.append(tools_menu)  
        # tools_menu_dropdown = Gtk.Menu()  
        # tools_menu.set_submenu(tools_menu_dropdown)   
        
        # # "工具" 菜单项
        # hosts_item = Gtk.MenuItem(label="Hosts 文件编辑器")  
        # hosts_item.connect("activate", self.run_hosts_file)  
        # tools_menu_dropdown.append(hosts_item)
        

        # "帮助" 菜单栏
        help_menu = Gtk.MenuItem(label="帮助")  
        menu_bar.append(help_menu)  
        help_menu_dropdown = Gtk.Menu()  
        help_menu.set_submenu(help_menu_dropdown)  

        # "帮助" 菜单项
        readme_item = Gtk.MenuItem(label="查看 README")
        readme_item.connect("activate", self.on_open_web, "https://github.com/CatIsNotFound/ShellToolbox")
        help_menu_dropdown.append(readme_item)
        github_item = Gtk.MenuItem(label="查看 Github 仓库")
        github_item.connect("activate", self.on_open_web, "https://github.com/CatIsNotFound/ShellToolbox")
        help_menu_dropdown.append(github_item)
        checkUpdate_item = Gtk.MenuItem(label="检查更新")
        checkUpdate_item.connect("activate", self.get_newer_version, pack_ver)
        help_menu_dropdown.append(checkUpdate_item)
        version_item = Gtk.MenuItem(label="查看当前版本号")
        version_item.connect("activate", self.get_version)
        help_menu_dropdown.append(version_item)

        # 创建笔记本  
        self.notebook = Gtk.Notebook()  
        box.pack_start(self.notebook, True, True, 10)  
  
        # 读取菜单
        try:
            menu_config = configparser.ConfigParser()
            with open(f"{appPath}/config/menu.ini", 'r', encoding='utf-8') as f:
                f.close()
            menu_config.read(f"{appPath}/config/menu.ini")
            group_items = menu_config.get('groups', 'items').strip('"').split(",")
            for group in group_items:
                box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
                tab_name = menu_config.get(group, 'name').strip('"')
                # print(tab_name)
                tab_items = menu_config.get(group, 'items').strip('"').split(",")
                for btn_item in tab_items:
                    btn_name = menu_config.get(btn_item, 'name').strip('"')
                    button = Gtk.Button(label=btn_name)
                    # print(f"    {btn_name}")
                    if 'run' in menu_config.options(btn_item):
                        run_command = menu_config.get(btn_item, 'run').strip('"')
                        button.connect("clicked", self.run_command, f'{appPath}{run_command}')
                    elif 'exec' in menu_config.options(btn_item):
                        run_command = menu_config.get(btn_item, 'exec').strip('"')
                        if 'warning' in menu_config.options(btn_item):
                            warn_text = menu_config.get(btn_item, 'warning').strip('"')
                            button.connect("clicked", self.run_subProcess, run_command, "warn", f"{warn_text}")
                        else:
                            button.connect("clicked", self.run_subProcess, run_command)

                    box.pack_start(button, True, True, 0)
                self.notebook.append_page(box, Gtk.Label(label=tab_name))
            if os.geteuid() == 0:
                self.show_warning_dialog("警告: 你正在以管理员身份（或 root 身份）运行工具箱, 请以普通用户下运行此工具！")
                quit()
                
            
        except Exception as e:
            self.show_error_dialog(f"Error: 找不到菜单或读取菜单时出现错误! 报错如下: \n{e}")
            quit()

    def on_quit(self, widget):  
        quit()
    
    def on_open_preference(self, widget):
        return_code = preference.main(f'{appPath}/config/setup.ini')
        if return_code == 127:
            self.show_error_dialog("Error: 未初始化配置, 无法获取配置信息! 请重新启动此软件! ")
        else:
            options()

    def on_button_clicked(self, widget, button_text):  
        print(f"正在执行：{button_text}") 

    def on_open_web(self, widget, url):
        n = self.show_question_dialog("即将使用浏览器访问外部网页，是否前往? ")
        if n == 1:
            if browser == 'firefox':
                self.run_command(self, f"/*/bin/firefox* {url}")
            elif browser == 'www':
                self.run_command(self, f"gnome-www-browser {url}")
            elif browser == 'chromium':
                self.run_command(self, f"chromium {url}")
            else:
                self.show_error_dialog("无法打开浏览器，请尝试修改 [首选项] >> [浏览方式]")
            # if return_code == 127:
            #     self.show_error_dialog("无法打开浏览器，请尝试修改 [首选项] >> [浏览方式]")

    def get_version(self, widget):
        self.show_info_dialog(f"版本号: {version_name}\n作者: CatIsNotFound\n使用 Bash Shell 编写脚本\n使用 GTK 3+ 编写 UI")
    
    def get_newer_version(self, widget, pack_version):        
        update_gui.show_gui(version_name, pack_version)


    # 打开终端以执行程序
    def run_command(self, widget, command):
        err = self.open_terminal(terminal, command)
        if err == 128:
            self.show_error_dialog(button_text="错误：找不到打开的终端或当前系统没有安装此终端！")
    
    # 执行外部程序
    def run_subProcess(self, widget, command, window_type='', text=""):
        if window_type == 'warn':
            self.show_warning_dialog(text)
        err = get_output(command, "stderr")
        if err != "":
            self.show_error_dialog(f"执行时发生错误, 输出内容如下: \n{err}")

    # 打开后台终端并执行脚本
    def open_terminal(self, terminal, operation):
        command = f'{appPath}/scripts/start_script.sh {terminal} {operation}'
        # print(f'正在执行：{command}')
        process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stderr = process.stderr.readline().decode()
        stdout = process.stdout.readline().decode()
        process.wait()
        if stdout == "128":
            self.show_error_dialog(f"Error: 执行时产生错误! (code: 128) \n错误内容如下: \n{stderr}")
        elif stdout == "127":
            self.show_error_dialog("Error: 未知的终端! 请选择其它终端! (code: 127)")
    
    # 显示问题对话框
    def show_question_dialog(self, button_text):
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
    def show_warning_dialog(self, button_text):
        warning_dialog = Gtk.MessageDialog(self,  
                                         0,  
                                         Gtk.MessageType.WARNING,  
                                         Gtk.ButtonsType.OK,  
                                         button_text)
        warning_dialog.run()  
        warning_dialog.destroy() 
    
    # 显示信息对话框
    def show_info_dialog(self, button_text):
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
    

# 用户配置文件
def options():
    global config
    global terminal
    global browser
    global appPath
    config = configparser.ConfigParser()
    if os.path.exists("config/setup.ini"):
        config.read('config/setup.ini')
        terminal = config.get('Config', 'terminal')
        appPath = config.get('Config', 'appPath')
        browser = config.get('Config', 'browser')
    else:
        # run_subprocess("sudo chmod -R u+x ./scripts/*.sh")
        appPath = get_output("pwd")
        terminal = get_output(f"{appPath}/scripts/get_terminal.sh")
        browser = get_output(f"{appPath}/scripts/get_browser.sh")
        config.add_section("Config")
        config.set("Config", "appPath", appPath)
        config.set("Config", "terminal", terminal)
        config.set("Config", "browser", browser)
        with open(f"{appPath}/config/setup.ini", 'w', encoding='utf-8') as file:
            config.write(file)
        file.close()

def get_output(command, outputmode="stdout"):
    process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stderr = process.stderr.readline().decode('utf-8')
    stdout = process.stdout.readline().decode('utf-8')
    process.wait()
    if outputmode == 'stdout':
        return stdout.strip()
    elif outputmode == 'stderr':
        return stderr.strip()
    elif outputmode == 'return':
        return process.returncode()


def run_outside_command(command, isShell=False):
    process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=isShell)
    # err = process.stderr.readline().decode('utf-8')
    process.wait()
    return process.returncode

def start(tag_name, pack_version):
    global version_name
    global pack_ver
    version_name = tag_name
    pack_ver = pack_version
    options()
    app = Application()  
    exit_status = app.run(sys.argv)  
    sys.exit(exit_status)
