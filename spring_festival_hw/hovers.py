from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/hovers")
"""
## 基礎練習 ##
1. Hovers
    url = "https://the-internet.herokuapp.com/hovers"
    *target = hover user1 and click "View Profile"
    hint: Hovers
"""

# 1. 定位「滑鼠要移上去」的那個容器（通常是頭像圖片）
avatar = driver.find_element(By.CLASS_NAME, "figure")

# 2. 執行懸停動作
actions = ActionChains(driver)
actions.move_to_element(avatar).perform()

# 3. 等待文字出現
wait = WebDriverWait(driver, 10)
user_name_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".figcaption h5")))

# 4. 取得文字 name 1 + 點擊下方的 view profile
print(user_name_element.text)
time.sleep(3)
driver.find_element(By.LINK_TEXT, "View profile").click()