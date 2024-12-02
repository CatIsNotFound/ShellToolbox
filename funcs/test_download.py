import tkinter as tk 
from tkinter import messagebox 
import threading 
import requests 
 
def download_file(url, filename): 
    response = requests.get(url)  
    with open(filename, 'wb') as file: 
        file.write(response.content)  
    messagebox.showinfo(" 下载完成", "文件已下载完成") 
 
def start_download(): 
    url = entry_url.get()  
    filename = entry_filename.get()  
    if url and filename: 
        threading.Thread(target=download_file, args=(url, filename)).start() 
    else: 
        messagebox.showwarning(" 输入错误", "请输入URL和文件名") 
 
# 创建主窗口 
root = tk.Tk() 
root.title(" 软件更新") 
 
# 创建输入框和标签 
tk.Label(root, text="下载URL:").grid(row=0, column=0) 
entry_url = tk.Entry(root) 
entry_url.grid(row=0,  column=1) 
 
tk.Label(root, text="文件名:").grid(row=1, column=0) 
entry_filename = tk.Entry(root) 
entry_filename.grid(row=1,  column=1) 
 
# 创建下载按钮 
tk.Button(root, text="下载更新", command=start_download).grid(row=2, column=0, columnspan=2) 
 
# 运行主循环 
root.mainloop()  