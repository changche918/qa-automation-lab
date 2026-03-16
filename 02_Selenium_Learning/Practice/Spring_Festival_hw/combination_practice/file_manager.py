import os
from datetime import datetime

class LogHandler:
    def __init__(): 
        pass
    def read_all_lines(self, file_path, num):
        """
        讀取檔案的指定行
        
        參數:
        - file_path: str, log 檔案完整路徑
        - num: int, 要讀取的行號（0 為第一行，-1 為最後一行）
        """
        if not os.path.exists(file_path):
            # with open(file_path, "w", encoding="utf-8") as file:
            #     file.write("[yyyy-mm-dd hh:mm:ss] 這是範例行。\n")
            print('no file')
            return False
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()  # 效果 : ['第一行內容\n', '第二行內容\n', '最後一行']
        if lines:
            readline = lines[num]
            return readline
        else:
            return None
        
    def read_file(self, file_path):
        """
        讀取整個檔案內容並印出
        
        參數:
        - file_path: str, log 檔案完整路徑
        """
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            print(f"讀取檔案內容:\n{content}")

    def write_log(self, file_path, data):
        """
        寫入一則 log 到檔案，並自動加上當下執行的時間
        
        參數:
        - file_path: str, log 檔案完整路徑
        - data: str, 欲寫入的訊息
        """
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("[yyyy-mm-dd hh:mm:ss] 這是範例行。\n")
        with open(file_path, "a", encoding="utf-8") as file:
            now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{now_time}] {data}\n")
            print(f"資料已成功寫入 {file_path}")