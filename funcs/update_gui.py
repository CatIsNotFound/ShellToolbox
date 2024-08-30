import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from funcs import update


class Update(Gtk.Window):
    def __init__(self):
        super().__init__(title="更新软件")
        
        self.set_default_size(600, 400)
        self.set_resizable(False)

        self.spinner = Gtk.Spinner()
        self.spinner.start()
        
        self.label = Gtk.Label(label="最新版本")

        self.scrolledwindow = Gtk.ScrolledWindow()
        self.scrolledwindow.set_hexpand(True)
        self.scrolledwindow.set_vexpand(True)
        self.textview = Gtk.TextView()
        self.textview.set_editable(False)
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text(f"asdasd\nasdasdasd")
        self.textbuffer.set_text(
            "This is some text inside of a Gtk.TextView. "
            + "Select text and click one of the buttons 'bold', 'italic', "
            + "or 'underline' to modify the text accordingly."
        )
        self.scrolledwindow.add(self.textview)

        self.btn_yes = Gtk.Button(label="下载更新")
        self.btn_yes.connect("clicked", self.on_btn_update)  
        self.btn_no = Gtk.Button(label="取消更新")
        self.btn_no.connect("clicked", self.on_btn_cancel)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)  
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.hbox.pack_end(self.btn_yes, False, False, 20)
        self.hbox.pack_end(self.btn_no, False, False, 5)

        self.vbox.pack_start(self.label, False, False, 5)
        self.vbox.pack_start(self.scrolledwindow, True, True, 5)
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
        #     opt = self.show_question_dialog(f"已找到最新版本({packs['tag_name']})，是否选择更新软件包？")
        #     if opt == 1:
        #         # get_pack_url(packs)
        #         # self.label.text("正在下载更新...")
        #         pack_url = update.get_pack_url(packs, 0)
        #         return_code = update.download_file(pack_url, pack_url.split("/")[-1])
        #         if return_code == 0:
        #             self.show_info_dialog("已下载完成，请重新启动软件!")
        #         else:
        #             self.show_error_dialog("下载软件包时出现错误! 请重试!")
        #         self.destroy()
            return None
        else:
            self.show_info_dialog("软件已是最新版本, 无需更新!")
            self.destroy()
            

    def on_btn_update(self, widget):
        if widget.get_label() != "正在更新":
            widget.set_label("正在更新")
            pack_url = update.get_pack_url(packs, 0)
            return_code = update.download_file(pack_url, pack_url.split("/")[-1])
            if return_code == 0:
                self.show_info_dialog("已下载完成，请重新启动软件!")
                quit()
            else:
                self.show_error_dialog("下载软件包时出现错误! 请检查网络或更换网络环境!")
                self.destroy()
        pass

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

def show_gui(version):
    global tag_ver
    global win    
    tag_ver = version
    win = Update()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()
    