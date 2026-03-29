from selenium.webdriver.common.by import By
import os
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from utils.find_high_gp import FindHighGP

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from utils.file_manager import FileHandler
from side_projects.utils.drivers import WebController

file_path = "side_projects/logs/madhead_post_log.txt"
content_path = "side_projects/logs/madhead_content_log.txt"

log = FileHandler()
driver_control = WebController()
finder = FindHighGP(driver_control)
# 20260322 初版 PR #10
# 20260324 調整程式寫法，使其可以取分頁 + GP PR #10
# 20260326 調整程式寫法，log.save 邏輯 PR #11
# 20260329 調整爆的寫法 PR #11
# 真實專案要爬的頁面
driver_control.get_url("https://forum.gamer.com.tw/B.php?bsn=23805")

# 測試用頁面
# driver.get("https://forum.gamer.com.tw/C.php?bsn=23805&snA=701544&tnum=240")
# driver.get("https://forum.gamer.com.tw/C.php?bsn=23805&snA=724765&tnum=81&bPage=8")

# 抓文章列表頁
wait = WebDriverWait(driver_control, 10)
articles = wait.until(
    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".b-list__row"))
)

titles = []
best_gp = -1  # 文章最少是 0，所以初始值給 -1 來比大小
best_art_elem = None

for art in articles:  # articles = 文章清單，art = 每篇文章
    if "b-list__row--sticky" not in art.get_attribute("class"):  # 排除置頂文
        try:
            title_elem = art.find_element(By.CSS_SELECTOR, ".b-list__main__title")
            gp_elem = art.find_element(By.CSS_SELECTOR, ".b-gp")
            gp_text = gp_elem.text

            if "爆" in gp_text:
                gp_value = float("inf")
            elif gp_text == "" or gp_text == "0":
                gp_value = 0
            else:
                gp_value = int(gp_text)

            # 文章 GP 比大小，印出超過 15 的
            # 用前面語法將 gp_text 轉成 gp_value，best_gp 是初始設定 -1，之後會被新的 gp_value 取代
            # if gp_value > 15:
            #     titles.append(f"[{gp_value}] {title_elem.text}")
            #     if gp_value > best_gp:
            #         best_gp = gp_value
            #         best_art_elem = title_elem

            # 另一種寫法比大小寫法
            if gp_value > 15:
                titles.append(f"[{gp_value}] {title_elem.text}")

            # 比較目前的 (best_gp, best_art_elem) 與新的 (gp_value, title_elem)
            # 取較大者並同時更新兩個變數
            best_gp, best_art_elem = max(
                (best_gp, best_art_elem), (gp_value, title_elem)
            )  # 20260327 比較 max 跟 if gp_value > best_gp:best_gp = gp_value

        except Exception as e:
            print(f"這樓跳過了，原因：{e}")  # 印出錯誤原因，但依然繼續跑下一輪

log.save_txt(file_path, titles)

if best_art_elem:
    best_art_elem.click()
    time.sleep(3)  # 等待跳轉
    current_page_url = driver_control.get_current_url
    log.save_txt(file_path, [f"文章網址: {current_page_url}"])

finder.scan_high_gp_content()  # 進到巴哈人氣最高文章後的第一頁，爬取人氣最高回覆
best_text = finder.scan_high_gp_content()
log.save_txt(content_path, best_text)

# 以下是換頁後 + 找到那頁 GP 最高的回覆文
while True:  # 使用無窮迴圈判斷切換分頁，滿足條件就跳出
    btns = driver_control.find_elements(
        By.CSS_SELECTOR, ".next"
    )  # 下一頁的按鈕元素 (是 list)
    no_next_button = driver_control.find_elements(
        By.CSS_SELECTOR, ".next.no"
    )  # 沒有下一頁的按鈕元素 (是 list)

    # 判斷 list 是否有東西
    if len(btns) > 0 and len(no_next_button) == 0:
        next_btn = btns[0]
        next_btn.click()
        time.sleep(5)
        print("換頁成功")
        best_text = finder.scan_high_gp_content()
        log.save_txt(content_path, best_text)
    else:
        print("完全找不到下一頁按鈕，停止")
        break

driver_control.close_windows
