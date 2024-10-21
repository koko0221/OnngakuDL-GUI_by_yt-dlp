import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from settings import SettingsWindow, load_settings, save_settings, load_history, save_history
from download import start_download

class YTDLPDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YT-DLP 極簡風音樂下載器")
        
        # 加載設定
        self.settings = load_settings('settings.json')
        
        # 加載歷史紀錄
        self.history = load_history('history.json')
        
        # 主畫面
        self.create_main_screen()
        
        # 進階設定頁面
        self.settings_window = SettingsWindow(self.root, self.settings, self.treeview)
        
        # 更新進階設定按鈕的命令
        self.advanced_settings_button.config(command=self.settings_window.show)
        
    #主畫面相關
    def create_main_screen(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)
        
        #標題/進階設定按鈕
        ttk.Label(main_frame, text="YT-DLP 極簡風音樂下載器").grid(row=0, column=0, columnspan=2, sticky="w")
        self.advanced_settings_button = ttk.Button(main_frame, text="進階設定", command=lambda: None)
        self.advanced_settings_button.grid(row=0, column=4)

        #空一列
        ttk.Label(main_frame, text="").grid(row=1, column=0, columnspan=5)
        
        #影片網址輸入框
        ttk.Label(main_frame, text="影片網址(支援批量/播放清單下載)").grid(row=2, column=0, columnspan=2, sticky="w")
        self.url_entry = tk.Text(main_frame, height=5, width=85)
        self.url_entry.grid(row=3, column=0, columnspan=5)
        
        # 輸入框加入提示文字
        self.url_entry.insert("1.0", "(輸入多個網址時，請確保每一行只有一個網址)")
        self.url_entry.bind("<FocusIn>", self.clear_placeholder)
        self.url_entry.bind("<FocusOut>", self.add_placeholder)
        
        #選擇音頻格式
        ttk.Label(main_frame, text="音頻格式").grid(row=4, column=0)
        self.format_combobox = ttk.Combobox(main_frame, values=["mp3", "m4a", "opus"])
        self.format_combobox.current(self.settings.get('default_format', 0))
        self.format_combobox.grid(row=4, column=1)
        
        #選擇下載路徑
        ttk.Label(main_frame, text="下載路徑").grid(row=4, column=2)
        self.path_entry = ttk.Entry(main_frame, width=30)
        self.path_entry.insert(0, self.settings.get('default_path', 'download'))
        self.path_entry.grid(row=4, column=3)
        ttk.Button(main_frame, text="選擇路徑", command=self.select_path).grid(row=4, column=4)
        
        #開始下載按鍵
        ttk.Button(main_frame, text="開始下載", command=self.start_download).grid(row=5, column=0, columnspan=5)
        
        #下載狀態與歷史紀錄表格
        self.create_download_table(main_frame)
        self.load_history() #讀取歷史紀錄

    #清除輸入框提示
    def clear_placeholder(self, event):
        if self.url_entry.get("1.0", tk.END).strip() == "(輸入多個網址時，請確保每一行只有一個網址)":
            self.url_entry.delete("1.0", tk.END)
    
    #恢復輸入框提示
    def add_placeholder(self, event):
        if not self.url_entry.get("1.0", tk.END).strip():
            self.url_entry.insert("1.0", "(輸入多個網址時，請確保每一行只有一個網址)")
    
    #下載狀態與歷史紀錄表格
    def create_download_table(self, frame):
        columns = ("影片名稱", "進度", "狀態")
        self.treeview = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.treeview.heading(col, text=col)
        self.treeview.grid(row=6, column=0, columnspan=5)
    
    #定義下載路徑
    def select_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    #開始下載
    def start_download(self):
        urls = self.url_entry.get("1.0", tk.END).strip().split('\n') #處理連結
        audio_format = self.format_combobox.get()
        download_path = self.path_entry.get()
    
        if not urls or not download_path:
            messagebox.showerror("錯誤", "請輸入正確影片網址和下載路徑") #排錯用
            return
    
        start_download(urls, audio_format, download_path, self.treeview) # 將下載相關資料傳送到download.py
    
    #讀取歷史紀錄函數
    def load_history(self):
        for record in self.history:
            self.treeview.insert('', 'end', values=record)
    
    #儲存歷史紀錄函數
    def save_history(self):
        records = [self.treeview.item(item, 'values') for item in self.treeview.get_children()]
        save_history('history.json', records)
        
if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)  # 禁用視窗縮放
    app = YTDLPDownloader(root)
    root.mainloop()
