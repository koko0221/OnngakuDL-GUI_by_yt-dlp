# OnngakuDL-GUI_by_yt-dlp

![ODL](http://this.website.com/cmoe?name=ODL&theme=mb)

- 基於 yt-dlp 的簡易音樂下載 GUI，大部分使用 AI 撰寫程式碼

- 理論上 Linux 也能運行，但沒有測試

- 尚有少量 Bug，應該不影響使用

## 功能

- 三種常用音樂格式可供選擇（大多串流媒體轉無損音檔意義不大，有損音檔是無法還原成無損的）：
  - **mp3**: 最通用
  - **m4a**: 表現較好
  - **opus**: YouTube 預設格式

- 自定義下載路徑
- 歷史紀錄紀錄
- 用戶配置記憶（在進階設定中可設置）

## 下載
以下檔案供 Windows 用戶使用，Mac 的用戶請直接運行代碼，或自行修改程式碼編譯：

- **[Onngaku-DL.zip](https://github.com/koko0221/OnngakuDL-GUI_by_yt-dlp/releases/latest/download/Onngaku-DL.zip)** 
  - 需自行下載 `ffmpeg.exe`並配置到目錄

- **[Onngaku-DL_ffmpeg_add.zip](https://github.com/koko0221/OnngakuDL-GUI_by_yt-dlp/releases/latest/download/Onngaku-DL_ffmpeg_add.zip)** 
  - 想直接使用請下載這個

## 使用 Python 運行:
### 與其花費時間做以下動作，不如直接配置[yt-dlp](https://github.com/yt-dlp/yt-dlp)會來得更值得!

1. 下載 Python
2. 下載 Git
3. 在 CMD（終端機）克隆專案：
   ``` shell
   git clone https://github.com/koko0221/OnngakuDL-GUI_by_yt-dlp.git
   ```
4. Windows 用戶下載 `ffmpeg.exe`，Mac 用戶下載 `ffmpeg` 到目錄，並確認 `download.py` 的 `ffmpeg_Path` 是否正確
5. cd 到目錄
6. 創建虛擬環境: 
   - Windows:
     ```
     py -m venv venv
     ```
   - Mac:
     ```
     python3 -m venv venv
     ```
7. 進入虛擬環境: 
   - Windows:
     ```
     source venv/bin/activate.ps1
     ```
   - Mac:
     ```
     source venv/bin/activate
     ```
8. 下載 tkinter（總之要確定有安裝）
9. 安裝 yt-dlp: `pip install yt-dlp`
10. 運行 `main.py`: 
    - Windows:
      ```
      py main.py
      ```
    - Mac:
      ```
      python3 main.py
      ```

## 預覽
<img width="834" alt="截圖 2024-10-21 上午11 41 44" src="https://github.com/user-attachments/assets/da74b4fa-ee50-49c5-8c19-b2f70038813e">
<img width="574" alt="截圖 2024-10-21 上午11 49 25" src="https://github.com/user-attachments/assets/53a62347-3876-43f6-a9cb-6921fcf4531d">
