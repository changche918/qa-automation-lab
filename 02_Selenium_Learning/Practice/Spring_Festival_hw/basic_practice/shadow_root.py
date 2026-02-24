from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/shadowdom")
""""
4. shadow-root
    url = https://the-internet.herokuapp.com/shadowdom
    *target = print: name="my-text"'s text (My default text)
    hint: shadow-root
"""
wait = WebDriverWait(driver, 10)

# # 1. 找到宿主元素 (Host)
# host = driver.find_element(By.CSS_SELECTOR, "my-paragraph")

# # 2. 取得 shadow_root
# root = host.shadow_root

# # 3. 在 shadow_root 內部尋找元素
# inner_p = root.find_element(By.CSS_SELECTOR, "slot")
# print(inner_p.text)

# 2026/2/24 加上 retry 寫法
for i in range(3):
    try:
        print(f"第 {i+1} 次抓取元素")
        
        # 1. 找到宿主元素 (Host)
        host = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "my-paragraph")))
        
        # 2. 取得 shadow_root
        root = host.shadow_root
        
        # 3. 在 shadow_root 內部尋找元素
        inner_p = root.find_element(By.CSS_SELECTOR, "slot")
        print(f"抓取成功，輸出為 : {inner_p.text}")
        break

    except TimeoutException:
        print("抓取超時：10 秒內沒看到目標元素")

    except NoSuchElementException:
        print("元素不存在")

    except Exception as e:
        print(f"其他未知錯誤: {e}")
else:
        print("已達到最大重試 3 次，抓取失敗。")