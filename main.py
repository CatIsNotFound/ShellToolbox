import gi  
gi.require_version('Gtk', '3.0')  
from gi.repository import Gtk 
import sys, subprocess, os, configparser


class AppWindow(Gtk.ApplicationWindow):  
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        self.set_title("快捷工具箱")  
        self.set_default_size(600, 180)  
        
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
        config_item.connect("activate", self.on_quit)  
        file_menu_dropdown.append(config_item)
        quit_item = Gtk.MenuItem(label="退出")  
        quit_item.connect("activate", self.on_quit)  
        file_menu_dropdown.append(quit_item) 
        
        # "帮助" 菜单栏
        help_menu = Gtk.MenuItem(label="帮助")  
        menu_bar.append(help_menu)  
        help_menu_dropdown = Gtk.Menu()  
        help_menu.set_submenu(help_menu_dropdown)  

        # "帮助" 菜单项
        readme_item = Gtk.MenuItem(label="查看 README")
        readme_item.connect("activate", self.on_open_web, "")
        help_menu_dropdown.append(readme_item)
        github_item = Gtk.MenuItem(label="查看 Github 仓库")
        github_item.connect("activate", self.on_quit)
        help_menu_dropdown.append(github_item)
        checkUpdate_item = Gtk.MenuItem(label="检查更新")
        checkUpdate_item.connect("activate", self.on_quit)
        help_menu_dropdown.append(checkUpdate_item)
        version_item = Gtk.MenuItem(label="查看当前版本号")
        version_item.connect("activate", self.on_quit)
        help_menu_dropdown.append(version_item)

        # 创建笔记本  
        self.notebook = Gtk.Notebook()  
        box.pack_start(self.notebook, True, True, 10)  
  
        # 读取菜单
        # try:
        menu_config = configparser.ConfigParser()
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
                elif 'box_yes' in menu_config.options(btn_item):
                    button.connect("clicked", self.messagebox, 1, menu_config.get())

                box.pack_start(button, True, True, 0)
            self.notebook.append_page(box, Gtk.Label(label=tab_name))
        # except BaseException:
        #     self.show_error_dialog("Error: 找不到菜单文件或无法读取菜单! \n(code: 128)")
        #     quit()

    def on_quit(self, widget):  
        quit()

    def on_button_clicked(self, widget, button_text):  
        print(f"正在执行：{button_text}") 

    def on_open_web(self, widget, url):
        n = self.show_question_dialog("即将使用浏览器访问外部网页，是否前往? ")
        if n == 1:
            run_outside_command(f"gnome-www-browser -- {url}")
            

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

# 用户配置文件
def options():
    config = configparser.ConfigParser()
    global terminal
    global appPath
    if os.path.exists("config/setup.ini"):
        config.read('config/setup.ini')
        terminal = config.get('Config', 'terminal')
        appPath = config.get('Config', 'appPath')
        config.clear()
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
        with open(f"{appPath}/config/setup.ini", 'w', encoding='utf-8') as file:
            file.write(context)
        file.close()

def get_output(command):
    process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.stdout.readline().decode('utf-8')
    process.wait()
    return output.strip()

def run_outside_command(command):
    process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == "__main__":  
    options()
    app = Application()  
    exit_status = app.run(sys.argv)  
    sys.exit(exit_status)
