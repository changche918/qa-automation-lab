import os
from datetime import datetime

class LogHandle:
    def __init__(self, filename, data=None, content=None):
        self.filename = filename
        self.data = data
        self.content = content

    def read_file(self):
        # 檢查檔案是否存在，避免程式崩潰
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                self.content = file.read()
                return self.content
        else:
            print(f"警告：找不到檔案 {self.filename}")
            return None
        
    def read_last_line(self):
        with open(self.filename, "r", encoding="utf-8") as file:
            lines = file.readlines() # 效果 : ['第一行內容\n', '第二行內容\n', '最後一行']
        if lines:  # 先檢查檔案是不是空的，避免報錯
            last_line = lines[-1]  # 取最後一筆並去掉換行符號
            return last_line
        else:
            return None
        
    def save(self, data):
        # 直接使用初始化時的 self.filename，或是從外面傳入
        with open(self.filename, "a", encoding="utf-8") as file:
            now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{now_time}] {data}\n")
            print(f"資料已成功寫入 {self.filename}")