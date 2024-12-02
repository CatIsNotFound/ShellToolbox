import gi
import os, threading

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from funcs import update
from funcs import main


class Update(Gtk.Window):
    def __init__(self):
        super().__init__(title="已发现最新版本")
        
        self.set_default_size(600, 400)
        self.set_resizable(False)

        self.spinner = Gtk.Spinner()
        self.spinner.start()
        
        self.label = Gtk.Label()
        self.tips = Gtk.Label()
        # self.tips.set_markup("<b>注意: 下载安装更新时，出现未响应等情况属于正常现象，请勿直接强制退出! </b>")

        self.scrolledwindow = Gtk.ScrolledWindow()
        self.scrolledwindow.set_hexpand(True)
        self.scrolledwindow.set_vexpand(True)
        self.textview = Gtk.TextView()
        self.textview.set_editable(False)
        self.textbuffer = self.textview.get_buffer()
        self.scrolledwindow.add(self.textview)

        self.btn_yes = Gtk.Button(label="前往下载页面")
        self.btn_yes.connect("clicked", self.on_btn_update)  
        self.btn_no = Gtk.Button(label="取消本次更新")
        self.btn_no.connect("clicked", self.on_btn_cancel)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)  
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.hbox.pack_end(self.btn_yes, False, False, 10)
        self.hbox.pack_end(self.btn_no, False, False, 5)

        self.vbox.pack_start(self.label, False, False, 5)
        self.vbox.pack_start(self.scrolledwindow, True, True, 5)
        self.vbox.pack_start(self.tips, False, False, 5)
        self.vbox.pack_end(self.hbox, False, False, 10)

        self.add(self.vbox)
        self.runner(tag_ver)

    def runner(self, version):
        global packs
        packs = update.check_update()
        self.label.set_markup(f"<b>{packs['name']}</b>")
        self.textbuffer.set_text(packs['body'])
        if update.is_newer_version(packs["tag_name"], version):
            self.show_all()
        else:
            self.show_all()
            self.show_info_dialog("软件已是最新版本, 无需更新!")
            self.destroy()

    def on_btn_update(self, widget): 
        # main.open_web("https://www.github.com/CatIsNotFound/ShellToolbox/releases")
        main_window = main.AppWindow()
        main_window.on_open_web(main_window, "https://www.github.com/CatIsNotFound/ShellToolbox/releases")
        

    def on_btn_cancel(self, widget):
        self.destroy()
    
    
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
    
    # 显示信息对话框
    def show_info_dialog(self, button_text):
        info_dialog = Gtk.MessageDialog(self,  
                                        0,  
                                        Gtk.MessageType.INFO,  
                                        Gtk.ButtonsType.OK,  
                                        button_text)  
        info_dialog.run()  
        info_dialog.destroy()

def show_gui(version, ver_type):
    global tag_ver
    global version_type
    tag_ver = version
    version_type = ver_type
    win = Update()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()
    