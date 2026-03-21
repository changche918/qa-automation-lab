import os
from datetime import datetime
import json

# 20260317 調整 function 寫法，擴充，及變數命名 PR #9
class FileHandler:
    def __init__(self): 
        pass
    def read_txt_lines(self, file_path, num_rows):
        """
        讀取 txt 檔案的指定行
        
        參數:
        - file_path: str, txt 檔案完整路徑
        - num_rows: int, 要讀取的行號（0 為第一行，-1 為最後一行）
        """
        if not os.path.exists(file_path):
            print('找不到檔案，請確認欲讀取的檔案是否存在')
            return False
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()  # 效果 : ['第一行內容\n', '第二行內容\n', '最後一行']
        if lines:
            readline = lines[num_rows]
            return readline
        else:
            return None
        
    def read_txt_file(self, file_path):
        """
        讀取整個 txt 檔案內容並印出
        
        參數:
        - file_path: str, log 檔案完整路徑
        """
        if not os.path.exists(file_path):
            print('找不到檔案，請確認欲讀取的檔案是否存在')
            return False
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            print(f"讀取檔案內容:\n{content}")

    def save_txt(self, file_path, data):
        """
        寫入一則 txt 到檔案，並自動加上當下執行的時間
        
        參數:
        - file_path: str, 檔案完整路徑
        - data: str, 欲寫入的訊息
        """
        if not os.path.exists(file_path):
            print('找不到檔案，請先手動建立檔案')
            return False
        with open(file_path, "a", encoding="utf-8") as file:
            now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{now_time}] {data}\n")
            print(f"資料已成功寫入 {file_path}")

    def save_json(self, data, file_path):
        """
        寫入一則 json 到檔案
        
        參數:
        - file_path: str, 檔案完整路徑
        - data: str, 欲寫入的訊息
        """
        if not os.path.exists(file_path):
            print('找不到檔案，請先手動建立檔案')
            return False
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            print(f"成功以 JSON 格式儲存至 {file_path}")

    def save_log(self):
        pass
    def save_png(self):
        pass