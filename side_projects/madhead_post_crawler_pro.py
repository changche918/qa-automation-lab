from selenium.webdriver.common.by import By
import os
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from utils.find_high_gp import FindHighGP

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",".."))
sys.path.append(project_root)

from utils.file_manager import FileHandler

file_path = "side_projects/logs/madhead_log.txt"
log = FileHandler()
driver = webdriver.Chrome()
finder = FindHighGP(driver)

# 真實專案要爬的頁面
driver.get("https://forum.gamer.com.tw/B.php?bsn=23805")

# 測試用頁面
# driver.get("https://forum.gamer.com.tw/C.php?bsn=23805&snA=698436&tnum=65&bPage=2")

wait = WebDriverWait(driver, 10)
articles = wait.until(
    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".b-list__row"))
)

titles = []
best_gp = -1
best_art_elem = None

for art in articles: # articles = 文章清單，art = 每篇文章
    if "b-list__row--sticky" not in art.get_attribute("class"):
        try:
            title_elem = art.find_element(By.CSS_SELECTOR, ".b-list__main__title")
            gp_elem = art.find_element(By.CSS_SELECTOR, ".b-gp")
            gp_text = gp_elem.text

            if gp_text == "爆":
                gp_value = 100
            elif gp_text == "" or gp_text == "0":
                gp_value = 0
            else:
                gp_value = int(gp_text)

            if gp_value > 15:
                titles.append(f"[{gp_value}] {title_elem.text}")
                if gp_value > best_gp:
                    best_gp = gp_value
                    best_art_elem = title_elem

        except Exception as e:
            print(f"這樓跳過了，原因：{e}")  # 印出錯誤原因，但依然繼續跑下一輪
            continue  # 程式不會停止，而是直接放棄這一輪，立刻執行下一輪，待優化。

log.save_txt(file_path, titles)

if best_art_elem:
    print(f"即將進入最高 GP ({best_gp}) 的文章")
    best_art_elem.click()
    time.sleep(3)  # 等待跳轉
    current_page_url = driver.current_url
    log.save_txt(file_path, [f"文章網址: {current_page_url}"])

finder.scan_high_gp_content() # 進到巴哈人氣最高頁，爬取人氣最高回覆

while True:  # 使用無窮迴圈判斷切換分頁，滿足條件就跳出
    btns = driver.find_elements(By.CSS_SELECTOR, ".next") #list，下一頁的按鈕元素
    no_next_button = driver.find_elements(By.CSS_SELECTOR, ".next.no") # list，沒有下一頁的按鈕元素
    
    # 判斷 list 是否有東西
    if len(btns) > 0 and len(no_next_button) == 0:
        next_btn = btns[0]
        next_btn.click()
        time.sleep(5)
        print("換頁成功")
        finder.scan_high_gp_content()
    else:
        print("完全找不到下一頁按鈕，停止")
        break

driver.quit()  # 關閉瀏覽器
