from selenium.webdriver.common.by import By
import os
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import random

# 20260321 新增巴哈姆特 - 神魔版，爬文章及標題 # PR 10
"""
TODO :
抓取綜合討論人氣 > 15 的文章，條件 :
    - 從最上面文章標題開始抓，直到符合 > 15 標準 # 20260322 debug mode 看為什麼出錯(抓到不要的文章)，is_display > 看失效在哪
    - 將該文章標題存起來
    - 點進去最高人氣那篇文章，將文章內容存下來
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

# 點擊 GP 的篩選
# list1 = driver.find_element(By.CSS_SELECTOR, '.b-list__filter__gp.is-select').click()
# driver.find_element(By.XPATH, "//select[@class='b-list__filter__gp is-select']//option[@value='200']").click()

articles = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".b-list__row")))

titles = []
best_gp = -1
best_gp_1 = -1
best_art_elem = None
best_post_id = ""

for art in articles:
     if "b-list__row--sticky" not in art.get_attribute("class"):
        try:
            title_elem = art.find_element(By.CSS_SELECTOR, ".b-list__main__title")
            gp_elem = art.find_element(By.CSS_SELECTOR, ".b-gp")
            gp_text = gp_elem.text

            # 處理 GP 數字：如果是「爆」或空值處理
            if gp_text == "爆":
                gp_value = 100 # 給它一個大數值
            elif gp_text == "" or gp_text == "0":
                gp_value = 0
            else:
                gp_value = int(gp_text) # 轉成整數才能做正確的數字比較

            if gp_value > 15:
            # 格式化存入
                titles.append(f"[{gp_value}] {title_elem.text}")
            # print(f"找到熱門文章：[{gp_value}] {title_elem.text}")
            # 紀錄目前最高的 GP 文章元素
                if gp_value > best_gp: # 程式中經典的「擂台賽（找最大值）」邏輯
                    best_gp = gp_value
                    best_art_elem = title_elem # 存下這個元素

        except Exception as e:
            continue

log.save_txt(file_path, titles)

if best_art_elem:
    print(f"即將進入最高 GP ({best_gp}) 的文章")
    best_art_elem.click()
    current_page_url = driver.current_url
    print(f"目前正在爬取的頁面：{current_page_url}")

    log.save_txt(file_path, current_page_url)
    
    # 文章內第一則回覆
    post_content = driver.find_elements(By.CSS_SELECTOR, ".c-article__content")[0].text

    log.save_txt(file_path, post_content)

    base_url = current_page_url 
    all_post_ids = []

    # page = 0 

    while True:
        try:
            posts = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".c-post")))
            a = driver.find_elements(By.CSS_SELECTOR, ".next")[0].click()

            time.sleep(random.uniform(2, 5))

            # 取得文章內各種回覆的 GP
            try:
                # 1. 抓取這頁所有的樓層區塊 (巴哈的樓層通常在 .c-section 內)
                posts = driver.find_elements(By.CSS_SELECTOR, "section[id^='post_']")
                
                best_gp = -1
                best_content = ""
                best_post_id = ""

                print(f"開始掃描本頁共 {len(posts)} 樓層...")

                for post in posts:
                    try:
                        # 2. 抓取該樓層的 GP 數
                        # GP 數字通常在 .get-gp .number 裡面
                        gp_elem = post.find_element(By.CSS_SELECTOR, ".get-gp .number")
                        gp_text = gp_elem.text.strip()

                        # 3. 處理 GP 數值（套用之前的邏輯）
                        if gp_text == "爆":
                            gp_value = 99999
                        elif not gp_text or gp_text == "0":
                            gp_value = 0
                        else:
                            # 只拿數字部分，處理像 "99+" 的情況
                            clean_gp = "".join(filter(str.isdigit, gp_text))
                            gp_value = int(clean_gp) if clean_gp else 0

                        # 4. 擂台賽：找出 GP 最高的樓層
                        if gp_value > best_gp:
                            best_gp = gp_value
                            best_post_id = post.get_attribute("id")
                            
                            # 抓取該樓層的文章內文 (.c-article__content)
                            # 有時候內文在 .c-post__body 內
                            try:
                                content_elem = post.find_element(By.CSS_SELECTOR, ".c-article__content")
                                best_content = content_elem.text
                            except:
                                best_content = "無法取得內文"

                    except Exception as e:
                        # 略過一些可能沒有 GP 的系統訊息樓層
                        continue

                    # 5. 最後印出結果
                    print("\n" + "="*50)
                    display_gp = "爆" if best_gp == 99999 else best_gp
                    print(f"🏆 本頁 GP 最高樓層 ID: {best_post_id}")
                    print(f"🔥 GP 點數: {display_gp}")
                    print("-" * 30)
                    print(f"內容摘要:\n{best_content[:300]}...") # 只印前 300 字
                    print("="*50)    

            finally:
                driver.quit()
        except NoSuchElementException:
                print("沒有下一頁了，停止")
                break
