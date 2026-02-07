from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


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
text_1 = driver.find_elements(By.CSS_SELECTOR, ".jb-link.jb-link-blue.h3")[0].text
text_1_href = driver.find_elements(By.CSS_SELECTOR, ".jb-link.jb-link-blue.h3")[0].get_attribute("href")
print(f"抓到的文字是 : {text_1} ,連結是 {text_1_href}")

text_2 = driver.find_elements(By.CSS_SELECTOR, ".category-item__text__name.d-block.h4")[0].text
text_2_href = driver.find_elements(By.CSS_SELECTOR, ".category-item__text__name.d-block.h4")[0].get_attribute("href")
print(f"抓到的文字是 : {text_2} ,連結是 {text_2_href}")

text_3 = driver.find_elements(By.CSS_SELECTOR, ".router-link-active.router-link-exact-active")[1].text
text_3_href = driver.find_elements(By.CSS_SELECTOR, ".router-link-active.router-link-exact-active")[1].get_attribute("href")
print(f"抓到的文字是 : {text_3} ,連結是 {text_3_href}")

text_4 = driver.find_elements(By.CSS_SELECTOR, ".btn.btn-sm.btn-outline-primary.mt-2.mt-md-7")[0].text
text_4_href = driver.find_elements(By.CSS_SELECTOR, ".btn.btn-sm.btn-outline-primary.mt-2.mt-md-7")[0].get_attribute("href")
print(f"抓到的文字是 : {text_4} ,連結是 {text_4_href}")

text_5 = driver.find_elements(By.CSS_SELECTOR, ".btn.btn-sm.btn-outline-primary.mt-2.mt-md-7")[1].text
text_5_href = driver.find_elements(By.CSS_SELECTOR, ".btn.btn-sm.btn-outline-primary.mt-2.mt-md-7")[1].get_attribute("href")
print(f"抓到的文字是 : {text_5} ,連結是 {text_5_href}")

with open("note.txt", "w", encoding="utf-8") as f:
    f.write(f"{text_1}\n")
    f.write(f"{text_1_href}\n")
    f.write(f"{text_2}\n")
    f.write(f"{text_2_href}\n")
    f.write(f"{text_3}\n")
    f.write(f"{text_3_href}\n")
    f.write(f"{text_4}\n")
    f.write(f"{text_4_href}\n")
    f.write(f"{text_5}\n")
    f.write(f"{text_5_href}\n")







driver.quit()