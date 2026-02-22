import logging

class LogManager:
    def __init__(self, log_file="automation.log"):
        # 1. 建立 logger
        self.logger = logging.getLogger("SeleniumCrawler")
        self.logger.setLevel(logging.INFO)
        
        # 2. 避免重複添加 Handler (防止 Log 重複印出)
        if not self.logger.handlers:
            # 設定輸出到檔案
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            # 設定輸出到控制台 (螢幕)
            stream_handler = logging.StreamHandler()
            
            # 設定格式：[時間] [層級] 內容
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
            file_handler.setFormatter(formatter)
            stream_handler.setFormatter(formatter)
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

    def info(self, msg): self.logger.info(msg)
    def error(self, msg): self.logger.error(msg)
    def warning(self, msg): self.logger.warning(msg)