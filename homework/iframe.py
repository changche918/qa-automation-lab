from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/iframe")
"""
2. IFrame 處理
    url = https://the-internet.herokuapp.com/iframe
    *target = print: id="tinymce"'s text (Your content goes here.)
    hint: iframe
"""

# 等待 iframe 出現並自動切換進去 (超方便的一步到位法)
WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "mce_0_ifr")))

# 現在已經在 iframe 裡面了，直接操作
# driver.click_element(By.CSS_SELECTOR, "div.tox-icon")
aaa = driver.find_element(By.CSS_SELECTOR, ".mce-content-body.mce-content-readonly p")
print(aaa.text)
# 結束後記得回來
driver.switch_to.default_content()