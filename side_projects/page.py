from selenium.webdriver.common.by import By
import os
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 這邊是寫換頁
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(project_root)

from utils.file_manager import FileHandler

file_path = "side_projects/logs/madhead_log.txt"
log = FileHandler()
driver = webdriver.Chrome()
driver.get("https://forum.gamer.com.tw/C.php?bsn=23805&snA=610529&tnum=23090")


# 等待文章出現
wait = WebDriverWait(driver, 10)

# 1. 確保這頁樓層載入
posts = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "section[id^='post_']")))
                    
# 2. 處理換頁 (重要：先抓完這頁再點下一頁)
while True:  # 使用無窮迴圈，內部再判斷何時跳出
    # 1. 抓取所有符合條件的按鈕 (回傳的是 list)
    btns = driver.find_elements(By.CSS_SELECTOR, ".next")

    # 2. 判斷 list 是否有東西
    if len(btns) > 0:
        next_btn = btns[0]
        next_btn.click()
        
        # 換頁後的等待非常重要，確保下一頁的 .next 載入
        time.sleep(5) 
        print('換頁成功')
    else:
        print("完全找不到下一頁按鈕，停止")
        break