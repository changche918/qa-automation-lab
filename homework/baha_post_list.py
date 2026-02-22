from selenium import webdriver
from selenium.webdriver.common.by import By

import homework.log_manager as log_manager

driver = webdriver.Chrome()
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
try:
    elem = driver.find_elements(By.CSS_SELECTOR, ('.b-list__main__title'))[3].text
    # elem = driver.find_elements(By.CSS_SELECTOR, '.b-list__main__title')
    # for i in range(4):
    #     target_elem = elem[3]  # 配合 i，第一圈拿 elem[0], 第二圈拿 elem[1]...
    #     print(target_elem.text)
        
    print(f"這次抓到的標題是 : {elem}")
    file_path = "homework\diff_log.txt"
    log = log_manager.LogHandle(file_path)
    # 如果 log 存在，執行以下
    # if os.path.exists(file_path):
    old_title = log.read()
        # with open(file_path, "r", encoding="utf-8") as file:
        #     old_title = file.read()
    print(f"上次存的標題是 :{old_title}")
    if (old_title.split("] ")[1].strip()) != elem: # 比對 log 檔的標題，跟新的標題一不一樣。加 strip 怕比對失敗
        
        print(f"不一樣! 這次的標題是{elem}")
        log.save(elem)
            # with open("homework\diff_log.txt", "w", encoding="utf-8") as file: # 如果 log 存在，且標題不一樣，就寫入
            #     now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # AI 提供
            #     file.write(f"[{now_time}] {elem}\n") #　AI 提供
    else: # 如果 log 不存在，執行這邊
        # log.save(elem)
        print('沒有不一樣，不更動檔案')
        # with open("homework\diff_log.txt", "w", encoding="utf-8") as file: # 如果 log 存在，且標題不一樣，就寫入
        #     now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # AI 提供
        #     # file.write(elem)
        #     file.write(f"[{now_time}] {elem}\n") #　AI 提供
        #     print(f"檔案不存在 or 新存入標題 :{elem}")

except Exception as e: # AI 提供
    screenshot_name = "error.png"
    driver.save_screenshot(screenshot_name) # AI 提供

    print("發生錯誤 :", e, "已截圖 :", screenshot_name )