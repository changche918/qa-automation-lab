from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
# import time

driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/hovers")

"""
## 基礎練習 ##
1. Hovers
    url = "https://the-internet.herokuapp.com/hovers"
    *target = hover user1 and click "View Profile"
    hint: Hovers

2/22 確認hovers為何錯誤    
"""
wait = WebDriverWait(driver, 10)

# # 1. 定位「滑鼠要移上去」的那個容器（通常是頭像圖片）
# avatar = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "figure")))

# # 2. 執行懸停動作
# actions = ActionChains(driver)
# actions.move_to_element(avatar).perform()

# # 3. 等待文字出現
# user_name_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".figcaption h5")))

# # 4. 取得文字 name 1 + 點擊下方的 view profile
# view_profile_text = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "View profile")))
# if view_profile_text.text == 'View profile':
#     view_profile_text.click()
#     print('成功點擊')
# else:
#     print('未成功點擊')



# 2026/2/24 加上 retry 寫法
for i in range(3):
    try:
        print(f"第 {i+1} 次抓取元素")
        # 1. 定位「滑鼠要移上去」的那個容器（通常是頭像圖片）
        avatar = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "figure")))

        # 2. 執行懸停動作
        actions = ActionChains(driver)
        actions.move_to_element(avatar).perform()

        # 3. 等待文字出現
        user_name_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".figcaption h5")))
        # time.sleep(2) # 測試滑鼠移開時，繼續重試
        # 4. 取得文字 name 1 + 點擊下方的 view profile
        view_profile_text = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "View profile")))
        if view_profile_text.text == 'View profile':
            view_profile_text.click()
            print('成功點擊')
            break

    except TimeoutException:
        print("抓取超時：10 秒內沒看到目標元素")
        driver.switch_to.default_content()

    except NoSuchElementException:
        print("元素不存在")
        driver.switch_to.default_content()
        
    except Exception as e:
        print(f"其他未知錯誤: {e}")
else:
        print("已達到最大重試 3 次，抓取失敗。")