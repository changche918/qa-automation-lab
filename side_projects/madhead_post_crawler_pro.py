from selenium.webdriver.common.by import By
import os
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 20260321 TODO
"""
抓取綜合討論人氣 > 15 的文章，條件 :
    - 從最上面文章標題開始抓，直到符合 > 15 標準
    - 將該文章標題存起來
    - 點進去那篇文章，將文章內容存下來
        - 文字 + URL https://forum.gamer.com.tw/C.php?bsn=23805&snA=729803&tnum=14
        - 並把所有留言的分頁掃完，抓 GP 最高的回覆內容印出來
"""
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(project_root)

from utils.file_manager import FileHandler

file_path = "side_projects/logs/madhead_log.txt"
log = FileHandler()
driver = webdriver.Chrome()
driver.get("https://forum.gamer.com.tw/B.php?bsn=23805")


# 等待文章出現
wait = WebDriverWait(driver, 10)
articles = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".b-list__row")))

titles = []

for art in articles:
    # 關鍵修正 1：加上 'not'，排除置頂文章
    if "b-list__row--sticky" not in art.get_attribute("class"):
        try:
            title_elem = art.find_element(By.CSS_SELECTOR, ".b-list__main__title")
            
            # 嘗試抓取 GP
            try:
                gp_elem = art.find_element(By.CSS_SELECTOR, ".b-list__summary .b-gp")
                gp_text = gp_elem.text
                
                # 處理 GP 數字：如果是「爆」或空值處理
                if gp_text == "爆":
                    gp_value = 100 # 給它一個大數值
                elif gp_text == "" or gp_text == "0":
                    gp_value = 0
                else:
                    gp_value = int(gp_text) # 轉成整數才能做正確的數字比較
            except:
                gp_value = 0

            # 關鍵修正 2：使用整數進行數字比較
            if gp_value > 15:
                # 格式化存入，這樣 log 才會漂亮
                titles.append(f"[{gp_value}] {title_elem.text}")
                print(f"找到熱門文章：[{gp_value}] {title_elem.text}")

        except Exception as e:
            # 防止單一文章抓取失敗導致整個程式中斷
            continue

# 最後再呼叫你的 function
log.save_txt(file_path, titles)