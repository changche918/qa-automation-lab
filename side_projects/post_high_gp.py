from selenium.webdriver.common.by import By
import os
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from find_high_gp import FindHighGP

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(project_root)

from utils.file_manager import FileHandler

file_path = "side_projects/logs/madhead_log.txt"
log = FileHandler()

driver = webdriver.Chrome()
finder = FindHighGP(driver) # 新的
# driver.get("https://forum.gamer.com.tw/B.php?bsn=23805")
driver.get("https://forum.gamer.com.tw/C.php?bsn=23805&snA=698436&tnum=65&bPage=2")

# wait = WebDriverWait(driver, 10)
# articles = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".b-list__row")))

# titles = []
# best_gp = -1
# best_art_elem = None

# for art in articles:
#      if "b-list__row--sticky" not in art.get_attribute("class"):
#         try:
#             title_elem = art.find_element(By.CSS_SELECTOR, ".b-list__main__title")
#             gp_elem = art.find_element(By.CSS_SELECTOR, ".b-gp")
#             gp_text = gp_elem.text

#             if gp_text == "爆":
#                 gp_value = 100
#             elif gp_text == "" or gp_text == "0":
#                 gp_value = 0
#             else:
#                 gp_value = int(gp_text)

#             if gp_value > 15:
#                 titles.append(f"[{gp_value}] {title_elem.text}")
#                 if gp_value > best_gp:
#                     best_gp = gp_value
#                     best_art_elem = title_elem 
#         except Exception:
#             continue

# log.save_txt(file_path, titles)

# if best_art_elem:
#     print(f"即將進入最高 GP ({best_gp}) 的文章")
#     best_art_elem.click()
#     time.sleep(3) # 等待跳轉
#     current_page_url = driver.current_url
#     log.save_txt(file_path, [f"文章網址: {current_page_url}"])

########################### 這邊是寫文章內，一頁的所有回覆比大小 ###########################
# 等待文章出現


finder.scan_high_gp_content()

# page_best_gp = -1
# page_best_content = "無內容"

# 1. 確保這頁樓層載入
# posts = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "section[id^='post_']")))


# # 2. 掃描本頁所有樓層
# for post in posts:
#     gp_elements = post.find_elements(By.CSS_SELECTOR, ".postgp")
    
#     if gp_elements:
#         gp_text = gp_elements[0].text.strip()

#         if "爆" in gp_text:
#             gp_value = 99999
#         else:
#             # AI 提供 - 只保留數字，過濾掉非數字字元
#             clean_gp = "".join(filter(str.isdigit, gp_text))
#             gp_value = int(clean_gp) if clean_gp else 0

#             if gp_value > page_best_gp:
#                 page_best_gp = gp_value
#                 try:
#                     page_best_content = post.find_element(By.CSS_SELECTOR, ".c-article__content").text
#                 except:
#                     page_best_content = "無法取得內文"

#         # print(f"找到 GP: {gp_text}")
#     else:
#         print("此樓層找不到 GP 標籤，跳過")

# print(f"本頁最高 GP 為: {page_best_gp}")
# # print(f"內容摘要:\n{page_best_content[:100]}...") # 只印前100字避免洗版
# print(f"內容摘要:\n{page_best_content}...") # 只印前100字避免洗版

###########################  這邊是寫換頁功能 ###########################
while True:  # 使用無窮迴圈，內部再判斷何時跳出
#     # 1. 抓取所有符合條件的按鈕 (回傳的是 list)
    btns = driver.find_elements(By.CSS_SELECTOR, ".next")
    no_next_button = driver.find_elements(By.CSS_SELECTOR, ".next.no")
    # 2. 判斷 list 是否有東西
    if len(btns) > 0 and len(no_next_button) == 0:
        next_btn = btns[0]
        next_btn.click()
        
        # 換頁後的等待非常重要，確保下一頁的 .next 載入
        time.sleep(5) 
        print('換頁成功')
        finder.scan_high_gp_content()
    else:
        print("完全找不到下一頁按鈕，停止")
        break
# 程式最後才關閉瀏覽器
driver.quit()


#         # 等待文章出現
#         wait = WebDriverWait(driver, 10)

#         page_best_gp = -1
#         page_best_content = "無內容"

#         # 1. 確保這頁樓層載入
#         posts = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "section[id^='post_']")))

#         # 2. 掃描本頁所有樓層
#         for post in posts:
#             gp_elements = post.find_elements(By.CSS_SELECTOR, ".postgp")
            
#             if gp_elements:
#                 gp_text = gp_elements[0].text.strip()

#                 if "爆" in gp_text:
#                     gp_value = 99999
#                 else:
#                     # AI 提供 - 只保留數字，過濾掉非數字字元
#                     clean_gp = "".join(filter(str.isdigit, gp_text))
#                     gp_value = int(clean_gp) if clean_gp else 0

#                     if gp_value > page_best_gp:
#                         page_best_gp = gp_value
#                         try:
#                             page_best_content = post.find_element(By.CSS_SELECTOR, ".c-article__content").text
#                         except:
#                             page_best_content = "無法取得內文"

#                 # print(f"找到 GP: {gp_text}")
#             else:
#                 print("此樓層找不到 GP 標籤，跳過")

#             print(f"本頁最高 GP 為: {page_best_gp}")
#             print(f"內容摘要:\n{page_best_content}...") # 只印前100字避免洗版

#     else:
#         print("完全找不到下一頁按鈕，停止")
#         break



