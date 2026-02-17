from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/hovers")
"""
## 基礎練習 ##
1. Hovers
    url = "https://the-internet.herokuapp.com/hovers"
    *target = hover user1 and click "View Profile"
    hint: Hovers
"""
driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/hovers")
# 1. 取得「元素物件」本身
target_element = driver.find_element(By.CSS_SELECTOR, ".figcaption")

# 2. 執行懸停 (Move to element 必須傳入物件)
actions = ActionChains(driver)
actions.move_to_element(target_element).perform()

# 3. 懸停後，取得該元素的文字進行判斷
element_text = target_element.text

if element_text == 'name: user1':
    target_element.click()  # 修正拼字：click
    print(f"已點擊：{element_text}")

print('aaa')
print(f"當前文字內容為：{element_text}")