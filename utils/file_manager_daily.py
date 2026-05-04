# Created: 2026-05-04
"""依日期自動分檔的 FileHandler 版本。

與 utils/file_manager.py 的差異：
1. 寫檔／讀檔時自動把檔名加上當天日期：
   logs/madhead_post_log.txt → logs/madhead_post_log_2026-05-04.txt
2. 上層資料夾不存在會自動建立（不再需要手動 mkdir）
3. 檔案不存在不會 return False，直接建新檔（save_txt 才不會跑一半失敗）

好處：
- 每天一個 log 檔，單檔大小被「一天的資料量」自然限制住
- 舊資料保留在硬碟，要查歷史紀錄直接看檔名日期
- call site 不用動，傳一樣的路徑即可

使用方式（call site 一行都不用改）：
    from utils.file_manager_daily import DailyFileHandler
    log = DailyFileHandler()
    log.save_txt("side_projects/logs/madhead_post_log.txt", titles)
    # 實際會寫入 side_projects/logs/madhead_post_log_2026-05-04.txt
"""
import os
import json
from datetime import datetime


class DailyFileHandler:
    def __init__(self):
        pass

    def _dated_path(self, file_path):
        """將 'foo/bar.txt' 轉成 'foo/bar_2026-05-04.txt'（加上今天日期後綴）。

        參數:
        - file_path: str, 原始檔案路徑
        回傳:
        - str, 加上今天日期後綴的新路徑
        """
        base, ext = os.path.splitext(file_path)
        today = datetime.now().strftime("%Y-%m-%d")
        return f"{base}_{today}{ext}"

    def _ensure_parent_dir(self, file_path):
        """確保上層資料夾存在；不存在則自動建立。

        參數:
        - file_path: str, 完整檔案路徑（含資料夾）
        """
        parent = os.path.dirname(file_path)
        if parent:
            os.makedirs(parent, exist_ok=True)

    def read_txt_lines(self, file_path, num_rows):
        """讀取當日 log 檔的指定行。

        參數:
        - file_path: str, 原始檔案路徑（內部會加上今天日期）
        - num_rows: int, 要讀取的行號（0 為第一行，-1 為最後一行）
        """
        dated = self._dated_path(file_path)
        if not os.path.exists(dated):
            print(f"找不到檔案 {dated}，請確認欲讀取的檔案是否存在")
            return False
        with open(dated, "r", encoding="utf-8") as file:
            lines = file.readlines()
        if lines:
            return lines[num_rows]
        return None

    def read_txt_file(self, file_path):
        """讀取整份當日 log 檔內容並印出。

        參數:
        - file_path: str, 原始檔案路徑（內部會加上今天日期）
        """
        dated = self._dated_path(file_path)
        if not os.path.exists(dated):
            print(f"找不到檔案 {dated}，請確認欲讀取的檔案是否存在")
            return False
        with open(dated, "r", encoding="utf-8") as file:
            content = file.read()
            print(f"讀取檔案內容:\n{content}")

    def save_txt(self, file_path, data):
        """寫入 txt 到當日 log 檔，並自動加上時間戳。

        資料夾與檔案不存在會自動建立。

        參數:
        - file_path: str, 原始檔案路徑（內部會加上今天日期）
        - data: str 或 list[str], 欲寫入的訊息
        """
        dated = self._dated_path(file_path)
        self._ensure_parent_dir(dated)
        with open(dated, "a", encoding="utf-8") as file:
            now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(data, list):
                for item in data:
                    file.write(f"[{now_time}]{item}\n")
            else:
                file.write(f"[{now_time}] {data}\n")
            print(f"資料已成功寫入 {dated}")

    def save_json(self, data, file_path):
        """寫入 JSON 到當日 log 檔。

        資料夾與檔案不存在會自動建立。

        參數:
        - data: 任意可序列化資料
        - file_path: str, 原始檔案路徑（內部會加上今天日期）
        """
        dated = self._dated_path(file_path)
        self._ensure_parent_dir(dated)
        with open(dated, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            print(f"成功以 JSON 格式儲存至 {dated}")
