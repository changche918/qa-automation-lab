import os
from datetime import datetime


class LogHandler:
    def read_all_lines(self, file_path, num):
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("[yyyy-mm-dd hh:mm:ss] 這是範例行。\n")
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()  # 效果 : ['第一行內容\n', '第二行內容\n', '最後一行']
        if lines:
            readline = lines[num]
            return readline
        else:
            return None

    def save(self, file_path, data):
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("[yyyy-mm-dd hh:mm:ss] 這是範例行。\n")
        with open(file_path, "a", encoding="utf-8") as file:
            now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{now_time}] {data}\n")
            print(f"資料已成功寫入 {file_path}")