from selenium.webdriver.common.by import By
from logger import LogManager
import os
import sys
import file_manager

# 20260307 調整變數名稱 PR #7

log = LogManager()
log.info("--- 啟動 Chrome 瀏覽器 ---")

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..", "..",".."))
sys.path.append(project_root)

from utils.drivers import WebController

finder = WebController()
log.info("正要前往巴哈姆特論壇，神魔之塔")
finder.get_url("https://forum.gamer.com.tw/B.php?bsn=23805")

screenshot_name = "combination_practice\screenshots\web_madhead.png"
finder.driver.save_screenshot(screenshot_name)
print("網頁已開啟並截圖 :", screenshot_name )

try:
    find_title_elem = finder.driver.find_elements(By.CSS_SELECTOR, ('.b-list__main__title'))[6].text
    
    file_path = "02_Selenium_Learning\Practice\Spring_Festival_hw\combination_practice\logs\madhead_change_log.txt"
    log = file_manager.LogHandler()

    last_log_line = log.read_all_lines(file_path, -1)
    
    if (last_log_line.split("] ")[1].strip()) != find_title_elem: # 比對 log 檔的標題，跟新的標題一不一樣。加 strip 怕比對失敗
        print(f"不一樣! 這次的標題是{find_title_elem}")
        # 檢查檔案，不存在則用 'a' (append) 模式開啟並立即關閉來建立它
        log.save(file_path, find_title_elem)
    else:
        print(f"這次抓到的標題是 : {find_title_elem}，沒有不一樣，不寫入 log")

except Exception as e: # AI 提供
    fail_screenshot_name = "screenshots\error_madhead.png"
    finder.driver.save_screenshot(fail_screenshot_name) # AI 提供

    print("發生錯誤 :", e, "已截圖 :", fail_screenshot_name )