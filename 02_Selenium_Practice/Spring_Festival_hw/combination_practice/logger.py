import logging
import os

class LogManager:
    def __init__(self, log_folder="logs", log_file="automation.log"):
        # 1. 確保資料夾存在 (避免 FileNotFoundError)
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        
        # 2. 合併路徑 (例如變成 "logs/automation.log")
        # 這樣寫能自動處理不同作業系統的斜線問題
        log_path = os.path.join(log_folder, log_file)
        
        # 3. 建立 logger
        self.logger = logging.getLogger("SeleniumCrawler")
        self.logger.setLevel(logging.INFO)
        
        # 4. 避免重複添加 Handler
        if not self.logger.handlers:
            # 正確傳入完整路徑 log_path
            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            stream_handler = logging.StreamHandler()
            
            # 設定格式
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
            file_handler.setFormatter(formatter)
            stream_handler.setFormatter(formatter)
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

    def info(self, msg): self.logger.info(msg)
    def error(self, msg): self.logger.error(msg)
    def warning(self, msg): self.logger.warning(msg)