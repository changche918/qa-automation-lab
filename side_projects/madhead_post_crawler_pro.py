from selenium.webdriver.common.by import By
import os
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 20260321 TODO
"""
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
list1 = driver.find_element(By.CSS_SELECTOR, '.b-list__filter__gp.is-select').click()
driver.find_element(By.XPATH, "//select[@class='b-list__filter__gp is-select']//option[@value='200']").click()

articles = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".b-list__row")))

titles = []
best_gp = -1
best_art_elem = None

for art in articles:
#     if "b-list__row--sticky" not in art.get_attribute("class"):
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
    
    post_content = driver.find_elements(By.CSS_SELECTOR, ".c-article__content")[0].text
    log.save_txt(file_path, post_content)

    base_url = current_page_url 
    all_post_ids = []

    page = 1

    while True:
        # base_url = https://forum.gamer.com.tw/C.php?bsn=23805&snA=610529&tnum=23087
        # page 1 = https://forum.gamer.com.tw/C.php?bsn=23805&page=1&snA=610529&tnum=23087
        # page 2 = https://forum.gamer.com.tw/C.php?bsn=23805&page=2&snA=610529&tnum=23087

        url = f"{base_url}&page={page}"
        print(f"抓第 {page} 頁")

        driver.get(url)
        posts = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".c-post")))

        # 抓 id
        for post in posts:
            post_id = post.get_attribute("id")  # 例如 post_360276123
            all_post_ids.append(post_id)

        # 判斷是否最後一頁（關鍵）
        # next_btn = driver.find_elements(By.CSS_SELECTOR, ".BH-pagebtnA a")
        # 如果你只想找該區域內的「a」標籤（按鈕本身）
        # next_btn = driver.find_elements(By.CSS_SELECTOR, '[data-gtm="C頁上方分頁"] a')[1] # 第 0 個不是

        # has_next = False
        # for btn in next_btn:
        #     if "下一頁" in btn.text:
        #         has_next = True
        #         break

        # if not has_next:
        #     print("已到最後一頁")
        #     break

        # page += 1

        # print(f"總共抓到 {len(all_post_ids)} 筆")
        # print(all_post_ids[:10])  # 先看前10筆
    