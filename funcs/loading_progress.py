import gi 
gi.require_version('Gtk',  '3.0') 
from gi.repository import Gtk
 
class UpdateWindow(Gtk.Window): 
    def __init__(self): 
        super().__init__(title="软件更新") 
        self.set_default_size(400,  50) 
 
        # 创建一个垂直盒子容器 
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10) 
        self.add(vbox)  
 
        # 创建一个进度条 
        self.label = Gtk.Label(label="Loading...")
        self.progressbar  = Gtk.ProgressBar()
        self.progressbar.set_pulse_setup()
        self.progressbar.pulse()

        vbox.pack_start(self.label,  True, True, 0) 
        vbox.pack_start(self.progressbar,  True, True, 0) 

        # 模拟更新进度 
        # self.timeout_id  = Gtk.timeout_add(100,  self.update_progress)  
        self.show_all()
        # self.update_progress()

    def update_progress(self): 
        new_value = self.progressbar.get_fraction()  + 0.01

        if new_value <= 1.0: 
            self.progressbar.set_fraction(new_value)  
            return True 
        else: 
            return False 
 
win = UpdateWindow() 
win.connect("destroy",  Gtk.main_quit)  
win.show_all()  
Gtk.main()  