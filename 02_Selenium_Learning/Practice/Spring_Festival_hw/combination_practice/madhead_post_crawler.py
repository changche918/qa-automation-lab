from selenium import webdriver
from selenium.webdriver.common.by import By
from logger import LogManager
from pathlib import Path

import file_manager

log = LogManager()
log.info("--- 啟動 Chrome 瀏覽器 ---")
driver = webdriver.Chrome()
log.info("正要前往巴哈姆特論壇，神魔之塔")
driver.get("https://forum.gamer.com.tw/B.php?bsn=23805")


screenshot_name = "combination_practice\screenshots\web_madhead.png"
driver.save_screenshot(screenshot_name)
print("網頁已開啟並截圖 :", screenshot_name )

try:
    raw_path = "02_Selenium_Learning\Practice\Spring_Festival_hw\combination_practice\logs\madhead_change_log.txt"
    file_path = Path(raw_path)
    log = file_manager.LogHandle(file_path)

    elem = driver.find_elements(By.CSS_SELECTOR, ('.b-list__main__title'))[6].text
    # file_path = "02_Selenium_Learning\Practice\Spring_Festival_hw\combination_practice\logs\madhead_change_log.txt"
    
    if not file_path.exists():
        file_path.touch()
        with open(raw_path, "w", encoding="utf-8") as file:
            file.write("[yyyy-mm-dd hh:mm:ss] 這是範例行。\n")

    old_title2 = log.read_last_line()
    
    if (old_title2.split("] ")[1].strip()) != elem: # 比對 log 檔的標題，跟新的標題一不一樣。加 strip 怕比對失敗
        print(f"不一樣! 這次的標題是{elem}")
        # 2. 檢查檔案，不存在則用 'a' (append) 模式開啟並立即關閉來建立它
        log.save(elem)
    else:
        print(f"這次抓到的標題是 : {elem}，沒有不一樣，不寫入 log")

except Exception as e: # AI 提供
    screenshot_name_fail = "screenshots\error_madhead.png"
    driver.save_screenshot(screenshot_name_fail) # AI 提供

    print("發生錯誤 :", e, "已截圖 :", screenshot_name_fail )