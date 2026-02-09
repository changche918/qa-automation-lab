from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

"""
TODO: 
1. 隱式等待與顯式等待 
2. 命名(可讀性) ex: text_1
3. debug "上市櫃"
4. **用迴圈嘗試**, 避免使用[0]這種
5. 修改json檔案的結構 hint: dict or list 
ex: 
  suit_job = {
    "適合你的好工作": {xxx}
  }
6. 抓元素可以嘗試用更清楚的 or 唯一值 or 不會變動的
7. 嘗試直接抓文字, 類似: text()="中高齡"
"""
"""
TODO: 
1. 到https://www.104.com.tw/網站 -> 找到五個區塊並逐一命名, 最少成印出文字+link(href)
    -> optimize hint: 能拆class/function | 能把區塊拆分更細 |
2. 存成txt檔案
    -> optimize hint: json格式的txt
"""
driver = webdriver.Chrome()
driver.get("https://www.104.com.tw/")
time.sleep(5)  # 等待網頁載入

### 職場新鮮事
# job_new_thing = driver.find_elements(By.CSS_SELECTOR, ".swiper-wrapper")
### 地區找工作
# area_find_job = driver.find_elements(By.CSS_SELECTOR, ".swiper-wrapper")

# print(len(area_find_job)) # 查看 area_find_job 裡面有多少值
# print(len(area_find_job))
# a = []
# for item in job_new_thing:
#     link = item.find_element(By.TAG_NAME, "a")
#     text = link.text()
#     href = link.get_attribute("href")
#     a.append((text, href))
# for item in job_new_thing:
#     link = item.find_element(By.TAG_NAME, "a")
#     # print(link.text)
#     if link.text == "AI推薦":
#         ai_link = link.get_attribute("href")
#         print(link.text, ai_link)
#     elif link.text == "月薪五萬起":
#         month_salary = link.get_attribute("href")
#         print(link.text, month_salary)
#     elif link.text == "遠距OK":
#         wfh_ok = link.get_attribute("href")
#         print(link.text, wfh_ok)
#     elif link.text == "無經驗可":
#         no_exp = link.get_attribute("href")
#         print(link.text, no_exp)

# results = []

# for item in job_new_thing:
#     link = item.find_element(By.TAG_NAME, "a")
#     text = link.text
#     href = link.get_attribute("href")

#     print(text, href)
#     results.append((text, href))
# data-gtm-index="搜尋欄位-header導流"

# results = {}

# for item in job_new_thing:
#     link = item.find_element(By.TAG_NAME, "a")

#     text = link.text.strip()
#     href = link.get_attribute("href")

#     results[text] = href

# for text, href in results.items():
#     print(text, href)



# with open("selenium\data.json", "w", encoding="utf-8") as file:
#     json.dump(data, file, indent=2, ensure_ascii=False)

parent = driver.find_element(
    By.CSS_SELECTOR,
    ".swiper.swiper-initialized.swiper-horizontal.swiper-backface-hidden"
)

items = parent.find_elements(By.CSS_SELECTOR, "a.category-item")

for item in items:
    title = item.find_element(
        By.CSS_SELECTOR,
        ".category-item__text__name"
    ).text

    desc = item.find_element(
        By.CSS_SELECTOR,
        ".category-item__text__desc"
    ).text

    print(title, desc)



driver.quit()