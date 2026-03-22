from selenium.webdriver.common.by import By
import os
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import random

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(project_root)

from utils.file_manager import FileHandler

file_path = "side_projects/logs/madhead_log.txt"
log = FileHandler()
driver = webdriver.Chrome()
driver.get("https://forum.gamer.com.tw/B.php?bsn=23805")

wait = WebDriverWait(driver, 10)
articles = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".b-list__row")))

titles = []
best_gp = -1
best_art_elem = None

for art in articles:
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
        except Exception:
            continue

log.save_txt(file_path, titles)

# --- 修正後的文章內爬取邏輯 ---
if best_art_elem:
    print(f"即將進入最高 GP ({best_gp}) 的文章")
    best_art_elem.click()
    time.sleep(3) # 等待跳轉
    
    current_page_url = driver.current_url
    log.save_txt(file_path, [f"文章網址: {current_page_url}"])
    
    # 建立跨頁擂台變數 (放在 while 外面才不會每頁重置)
    overall_best_gp = -1
    overall_best_content = ""

    while True:
        try:
            # 1. 確保這頁樓層載入
            posts = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "section[id^='post_']")))
            
            # 2. 掃描本頁所有樓層
            for post in posts:
                try:
                    gp_elem = post.find_element(By.CSS_SELECTOR, ".get-gp .number")
                    gp_text = gp_elem.text.strip()

                    # GP 轉換邏輯
                    if gp_text == "爆":
                        gp_value = 99999
                    else:
                        clean_gp = "".join(filter(str.isdigit, gp_text))
                        gp_value = int(clean_gp) if clean_gp else 0

                    # 跨頁比較最大值
                    if gp_value > overall_best_gp:
                        overall_best_gp = gp_value
                        try:
                            overall_best_content = post.find_element(By.CSS_SELECTOR, ".c-article__content").text
                        except:
                            overall_best_content = "無法取得內文"
                except:
                    continue

            # 3. 處理換頁 (重要：先抓完這頁再點下一頁)
            next_btns = driver.find_elements(By.CSS_SELECTOR, ".BH-pagebtnA a.next")
            if next_btns:
                next_btns[0].click()
                print("前往下一頁...")
                time.sleep(random.uniform(3, 5)) # 隨機延遲預防封鎖
            else:
                print("沒有下一頁了，停止")
                break

        except (NoSuchElementException, TimeoutException):
            print("換頁異常或結束")
            break

    # 4. 全部頁面跑完後存檔
    log.save_txt(file_path, [f"全篇最高 GP ({overall_best_gp}):", overall_best_content])

# 程式最後才關閉瀏覽器
driver.quit()