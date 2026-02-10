from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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
wait = WebDriverWait(driver, 10)

# 1.先抓「適合你的好工作」這整塊
job_recommend_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.box-container.job-recommend")))

# 2.只在這塊裡面抓 tab 的 a
tabs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.box-container.job-recommend .tabs .row.tabbar a")))

for job_list in tabs:
    print(job_list.text, "=>", job_list.get_attribute("href"))

# 這一行會讓 json 再包一層
data = {"適合你的好工作": {job_list.text: job_list.get_attribute("href")for job_list in tabs}}

with open("selenium\data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)

driver.quit()
