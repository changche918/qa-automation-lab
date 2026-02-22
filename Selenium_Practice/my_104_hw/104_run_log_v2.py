from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import data_manager

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

# 1.只在「適合你的好工作」這塊裡面抓 tab 的 a
# 這是顯式等待
tabs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.box-container.job-recommend .tabs .row.tabbar a")))
for job_list in tabs:
    print(job_list.text, "=>", job_list.get_attribute("href"))

# 職場新鮮事
job_new_thing = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".title.h1"))
)

# 抓出跟履歷撰寫同一層的其他選項
element = driver.find_element(
    By.XPATH, "//a[contains(@data-gtm-index,'履歷撰寫')]"
)
parent = element.find_element(By.XPATH, "./..")   # 回到父層才能抓他下面全部
other_thing = parent.find_elements(By.TAG_NAME, "a")

for sub in other_thing:
    print(sub.text, "=>", sub.get_attribute("href"))

data_manager.DataSaver(title="適合你的好工作").save(tabs, "selenium\data_1.json")
data_manager.DataSaver(title="職場新鮮事").save(other_thing, "selenium\data_2.json")

# 關閉瀏覽器
driver.quit()
