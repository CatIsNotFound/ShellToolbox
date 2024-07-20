import gi  
gi.require_version('Gtk', '3.0')  
from gi.repository import Gtk  
  
class MyWindow(Gtk.Window):  
    def __init__(self):  
        super().__init__(title="GTK3+ Menu Example")  
        self.set_default_size(400, 300)  # 设置窗口的默认大小  
  
        # 使用Gtk.Box作为布局容器  
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)  
        self.add(box)  
  
        # 创建菜单栏并添加到布局容器中  
        menu_bar = Gtk.MenuBar()  
        box.pack_start(menu_bar, False, False, 0)  
  
        # 创建“文件”菜单及其菜单项  
        file_menu = Gtk.MenuItem(label="File")  
        menu_bar.append(file_menu)  
        file_menu_dropdown = Gtk.Menu()  
        file_menu.set_submenu(file_menu_dropdown)  
  
        # 添加菜单项到“文件”菜单  
        open_item = Gtk.MenuItem(label="Open")  
        open_item.connect("activate", self.on_open)  
        file_menu_dropdown.append(open_item)  
  
        quit_item = Gtk.MenuItem(label="Quit")  
        quit_item.connect("activate", self.on_quit)  
        file_menu_dropdown.append(quit_item)  
  
        # 添加一个标签作为窗口的其他内容  
        label = Gtk.Label(label="This is the main content of the window.")  
        box.pack_start(label, True, True, 10)  # 使用pack_start添加标签，并设置其扩展和填充属性  
  
    def on_open(self, widget):  
        print("Open clicked")  
  
    def on_quit(self, widget):  
        Gtk.main_quit()  
  
def main():  
    app = MyWindow()  
    app.connect("delete-event", Gtk.main_quit)  
    app.show_all()  
    Gtk.main()  
  
if __name__ == "__main__":  
    main()