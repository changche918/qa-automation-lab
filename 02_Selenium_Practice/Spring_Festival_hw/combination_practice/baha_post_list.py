from selenium import webdriver
from selenium.webdriver.common.by import By
from logger import LogManager

import file_manager

log = LogManager()
log.info("--- 啟動 Chrome 瀏覽器 ---")
driver = webdriver.Chrome()
log.info("正要前往巴哈姆特論壇，天堂版")
driver.get("https://forum.gamer.com.tw/B.php?bsn=84452")

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
    hint: for loop (???), if-else, class, function, file-control(ex: with), os(for example)
"""
screenshot_name = "screenshots\web.png"
driver.save_screenshot(screenshot_name)
print("網頁已開啟並截圖 :", screenshot_name )

try:
    elem = driver.find_elements(By.CSS_SELECTOR, ('.b-list__main__title'))[3].text
    
    file_path = "logs\change_log.txt"
    log = file_manager.LogHandle(file_path)
    old_title2 = log.read_last_line()
    
    if (old_title2.split("] ")[1].strip()) != elem: # 比對 log 檔的標題，跟新的標題一不一樣。加 strip 怕比對失敗
        print(f"不一樣! 這次的標題是{elem}")
        log.save(elem)
    else: # 如果 log 不存在，執行這邊
        print(f"這次抓到的標題是 : {elem}，沒有不一樣，不寫入 log")

except Exception as e: # AI 提供
    screenshot_name_fail = "screenshots\error.png"
    driver.save_screenshot(screenshot_name_fail) # AI 提供

    print("發生錯誤 :", e, "已截圖 :", screenshot_name_fail )