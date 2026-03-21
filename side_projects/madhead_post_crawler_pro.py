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

file_path = "side_projects\logs\madhead_log.txt"
log = FileHandler()
driver = webdriver.Chrome()
driver.get("https://forum.gamer.com.tw/B.php?bsn=23805")


# 等待文章出現
wait = WebDriverWait(driver, 10)
articles = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".b-list__row")))

titles = []

for art in articles:
    # 檢查該 row 的 class 屬性中是否包含 'm-sticky' (以巴哈姆特為例)
    # 或者檢查是否有置頂圖示的 class
    if "b-list__row b-list__row--sticky" in art.get_attribute("class"):
        continue  # 如果是置頂，就跳過這一次迴圈
        
    try:
        title_elem = art.find_element(By.CSS_SELECTOR, ".b-list__main__title")
        original_title = title_elem.text
        titles.append(f"[{title_elem.text}] {title_elem.text}\n")
        
    except:
        continue

log.save_txt(file_path, titles)
print(titles)