import yt_dlp
from tkinter import messagebox, ttk
import threading
import json
import os
import queue

def start_download(urls, audio_format, download_path, treeview):
    download_queue = queue.Queue()

    def download_worker():
        while True:
            url = download_queue.get()
            if url is None:
                break
            download(url)
            download_queue.task_done()

    def download(url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'ffmpeg_location': os.path.realpath('ffmpeg'), #yt-dlp PATH, Windows的話是'ffempeg.exe', Mac的話是'ffmpeg'
            'outtmpl': f'{download_path}/%(title)s.%(ext)s',
            'writethumbnail': True,  # 下載縮圖
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': audio_format, #音檔格式
                },
                {
                    'key': 'FFmpegMetadata', #追加影片資料
                    'add_metadata': True,
                },
                {
                    'key': 'EmbedThumbnail',
                    'already_have_thumbnail': False,
                }
            ],
            'progress_hooks': [lambda d: update_progress(d, treeview)],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                title = info_dict.get('title', None)
                if title is None:
                    raise Exception("無法獲取影片標題，可能是私人影片或無權限訪問。")
                if 'entries' in info_dict:
                    for entry in info_dict['entries']:
                        ydl.download([entry['webpage_url']])
                else:
                    ydl.download([url])
            update_history(treeview, "成功")

        except Exception as e:
            update_history(treeview, "失敗")
            messagebox.showerror("錯誤", f"下載失敗: {url}\n錯誤訊息: {e}")

    # 將所有URL加入佇列
    for url in urls:
        url = url.strip()
        if url:
            download_queue.put(url)

    # 啟動下載工作執行緒
    threading.Thread(target=download_worker).start()

#下載狀態與歷史紀錄表格
def update_progress(d, treeview):
    if d['status'] == 'downloading':
        percent = d['_percent_str']
        speed = d['_speed_str']
        #處理檔案路徑，只留下檔名
        title_PATH = d['filename']
        title_with_extension = os.path.basename(title_PATH)
        title, _ = os.path.splitext(title_with_extension)

        # 更新表格中的進度
        for item in treeview.get_children():
            if treeview.item(item, 'values')[0] == title:
                treeview.item(item, values=(title, f"{percent} ({speed})", "下載中"))
                break
        else:
            treeview.insert('', 'end', values=(title, f"{percent} ({speed})", "下載中"))

    #下載成功
    elif d['status'] == 'finished':
        title_PATH = d['filename']
        title_with_extension = os.path.basename(title_PATH)
        title, _ = os.path.splitext(title_with_extension)
        for item in treeview.get_children():
            if treeview.item(item, 'values')[0] == title:
                # 檢查是否有錯誤訊息
                if 'error' in d:
                    treeview.item(item, values=(title, '100%', f"失敗: {d['error']}"))
                else:
                    treeview.item(item, values=(title, '100%', "成功"))
                break
        else:
            if 'error' in d:
                treeview.insert('', 'end', values=(title, '100%', f"失敗: {d['error']}"))
            else:
                treeview.insert('', 'end', values=(title, '100%', "成功"))

# 更新歷史紀錄
def update_history(treeview, status):
    records = [treeview.item(item, 'values') for item in treeview.get_children()]
    for record in records:
        if record[2] == "下載中":
            record[2] = status
    print(f"儲存歷史紀錄: {records}")  # 除錯訊息
    save_history('history.json', records)

# 儲存歷史紀錄
def save_history(file_path, history):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(history, file, ensure_ascii=False, indent=4)
        print(f"歷史紀錄已儲存至 {file_path}")  # 除錯訊息
    except Exception as e:
        print(f"儲存歷史紀錄失敗: {e}")  # 除錯訊息
