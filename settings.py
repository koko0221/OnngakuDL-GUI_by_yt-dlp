import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

#建立設定頁面視窗
class SettingsWindow:
    def __init__(self, root, settings, treeview):
        self.settings = settings
        self.treeview = treeview
        self.advanced_settings = tk.Toplevel(root)
        self.advanced_settings.title("進階設定")
        self.advanced_settings.withdraw()  # 初始化時隱藏視窗
        self.advanced_settings.protocol("WM_DELETE_WINDOW", self.on_closing)  # 監聽視窗關閉事件
        
        #預設格式(僅初始化時讀取)
        ttk.Label(self.advanced_settings, text="預設格式").grid(row=0, column=0, sticky="w")
        self.default_format_combobox = ttk.Combobox(self.advanced_settings, values=["mp3", "m4a", "opus"])
        self.default_format_combobox.current(self.settings.get('default_format', 0))
        self.default_format_combobox.grid(row=0, column=1, sticky="w")
        
        #預設下載目錄(僅初始化時讀取)
        ttk.Label(self.advanced_settings, text="預設下載目錄").grid(row=1, column=0)
        self.default_path_entry = ttk.Entry(self.advanced_settings, width=30)
        self.default_path_entry.insert(0, self.settings.get('default_path', 'download'))
        self.default_path_entry.grid(row=1, column=1)
        ttk.Button(self.advanced_settings, text="選擇路徑", command=self.select_default_path).grid(row=1, column=2)
        
        #儲存配置
        ttk.Button(self.advanced_settings, text="儲存", command=self.save_settings).grid(row=2, column=0, columnspan=3)
        #刪除所有歷史紀錄
        ttk.Button(self.advanced_settings, text="刪除歷史紀錄", command=self.clear_history).grid(row=3, column=0, columnspan=3)
        
    def show(self):
        self.advanced_settings.deiconify()
        
    def on_closing(self):
        self.advanced_settings.withdraw()  # 隱藏視窗而不是銷毀

    #預設下載目錄(僅初始化時讀取)
    def select_default_path(self):
        path = filedialog.askdirectory()
        if path:
            self.default_path_entry.delete(0, tk.END)
            self.default_path_entry.insert(0, path)
    
    #儲存配置
    def save_settings(self):
        self.settings['default_format'] = self.default_format_combobox.current()
        self.settings['default_path'] = self.default_path_entry.get()
        save_settings('settings.json', self.settings)
        messagebox.showinfo("完成", "設定已儲存")
    
    #刪除所有歷史紀錄
    def clear_history(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        save_history('history.json', [])
        messagebox.showinfo("完成", "歷史紀錄已刪除")

#讀取設定
def load_settings(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

#儲存配置
def save_settings(file_path, settings):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(settings, file, ensure_ascii=False, indent=4)

#讀取歷史紀錄
def load_history(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

#儲存歷史紀錄
def save_history(file_path, history):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(history, file, ensure_ascii=False, indent=4)
