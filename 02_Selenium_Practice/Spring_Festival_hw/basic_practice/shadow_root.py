from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/shadowdom")
""""
4. shadow-root
    url = https://the-internet.herokuapp.com/shadowdom
    *target = print: name="my-text"'s text (My default text)
    hint: shadow-root
"""
# 1. 找到宿主元素 (Host)
host = driver.find_element(By.CSS_SELECTOR, "my-paragraph")

# 2. 取得 shadow_root
root = host.shadow_root

# 3. 在 shadow_root 內部尋找元素 (例如裡面那個 <p> 標籤)
inner_p = root.find_element(By.CSS_SELECTOR, "slot")
print(inner_p.text)