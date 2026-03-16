from selenium.webdriver.common.by import By
from logger import LogManager
import os
import sys
import file_manager

# 20260307 調整變數名稱 PR #7
"""
## 組合練習 ##
1. 偵測內容(範例: 第一個class=b-list__row b-list-item b-imglist-item有無更新, 此整行有無更新, 若有時間可嘗試更細的判斷)
    url = ex: https://forum.gamer.com.tw/B.php?bsn=84452
    要求: 
        1. 使用hint提及內容
        2. 將selenium driver獨立檔案使用(function)
        3. 當程式錯誤時, 當下截圖並存下(capture)
        4. 判斷重要資訊(人的帳號)是否更新或不同(.env), 環境變數使用ex: os.environ.get #此項真的做不出來沒關係
    每次執行時:
        - 確認log檔案是否存在: 
            - 不存在: 存下內容 | 存在: 對比差異
    若有不同:
        - 印出差異
        - 存下差異
        - 修改原先log
    hint: for loop, if-else, class, function, file-control(ex: with), os(for example)
"""

log = LogManager()
log.info("--- 啟動 Chrome 瀏覽器 ---")

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..", "..",".."))
sys.path.append(project_root)

from utils.drivers import WebController

finder = WebController()
log.info("正要前往巴哈姆特論壇，天堂版")
finder.get_url("https://forum.gamer.com.tw/B.php?bsn=84452")

screenshot_name = "combination_practice\screenshots\web.png"
finder.driver.save_screenshot(screenshot_name)
print("網頁已開啟並截圖 :", screenshot_name )

try:
    find_title_elem = finder.driver.find_elements(By.CSS_SELECTOR, ('.b-list__main__title'))[3].text
    
    file_path = "02_Selenium_Learning\Practice\Spring_Festival_hw\combination_practice\logs\change_log.txt"
    log = file_manager.LogHandler()
    last_log_line = log.read_all_lines(file_path, -1)
    
    if (last_log_line.split("] ")[1].strip()) != find_title_elem: # 比對 log 檔的標題，跟新的標題一不一樣。加 strip 怕比對失敗
        print(f"不一樣! 這次的標題是{find_title_elem}")
        log.write_log(file_path, find_title_elem)
    else:
        print(f"這次抓到的標題是 : {find_title_elem}，沒有不一樣，不寫入 log")

except Exception as e: # AI 提供
    fail_screenshot_name = "screenshots\error.png"
    finder.driver.save_screenshot(fail_screenshot_name) # AI 提供

    print("發生錯誤 :", e, "已截圖 :", fail_screenshot_name )