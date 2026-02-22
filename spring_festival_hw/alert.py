from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/javascript_alerts")
"""
3. Alert / Confirm 對話框
    url = https://the-internet.herokuapp.com/javascript_alerts
    *target = click all btn, finally print (id="result")'s text
    hint: handle pop-up
"""
driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click() # 1. 先點擊按鈕觸發 Alert
time.sleep(1)
alert1 = driver.switch_to.alert # 2. 將控制權切換到 Alert
print(f"警示框內容是: {alert1.text}") # 3. 取得 Alert 上的文字內容
alert1.accept() # 4. 點擊「確定」 (Accept)

driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']").click()
time.sleep(1)
alert2 = driver.switch_to.alert
print(f"警示框內容是: {alert1.text}")
alert2.accept()

driver.find_element(By.XPATH, "//button[text()='Click for JS Prompt']").click()
time.sleep(1)
alert3 = driver.switch_to.alert
print(f"警示框內容是: {alert1.text}")
alert3.accept()

result_text = driver.find_element(By.ID, "result")
print (result_text.text)

driver.quit()
