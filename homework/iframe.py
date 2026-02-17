from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/iframe")
"""
2. IFrame 處理
    url = https://the-internet.herokuapp.com/iframe
    *target = print: id="tinymce"'s text (Your content goes here.)
    hint: iframe
"""