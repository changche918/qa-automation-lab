from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..", "..",".."))
sys.path.append(project_root)

from utils.drivers import WebController

finder = WebController()
finder.get_url("https://the-internet.herokuapp.com/javascript_alerts")
# wait = WebDriverWait(finder.driver, 10)

"""
3. Alert / Confirm 對話框
    url = https://the-internet.herokuapp.com/javascript_alerts
    *target = click all btn, finally print (id="result")'s text
    hint: handle pop-up
"""
# 20260226 優化程式，使用 for 迴圈執行 find_element
# 20260302 調整變數名稱 PR #4
# 20260305 加上引用 drivers function，並調整 alert 原本寫法 PR #6


for i in range(3):
    try:
        alert_elem = finder.visit_elem(By.XPATH, "//button[text()='Click for JS Alert']")
        confirm_elem = finder.visit_elem(By.XPATH, "//button[text()='Click for JS Confirm']")
        prompt_elem = finder.visit_elem(By.XPATH, "//button[text()='Click for JS Prompt']")
        
        # alert_elem = wait.until(EC.element_to_be_((By.XPATH, "//button[text()='Click for JS Alert']")))
        # confirm_elem = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Confirm']")))
        # prompt_elem = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Prompt']")))
        
        javascript_alerts = [alert_elem, confirm_elem, prompt_elem]
        
        for button in javascript_alerts:
            button.click()
            alert_title = finder.wait_alert()
            print(f"警示框內容是 : {alert_title.text}")
            alert_title.accept()
        
        '''暫保留以下寫法 (以便比對新舊寫法)
        # prompt_elem.click()
        # alert_third = finder.alert_switch
        
        # alert_third.send_keys("My's Ryan")
        # alert_third.accept()
        '''
        prompt_elem.click() # 只對 prompt alert 做操作
        # alert_box = WebDriverWait(finder.driver, 10).until(EC.alert_is_present())
        alert_box = finder.wait_alert()
        alert_box.send_keys("My's Ryan")
        alert_box.accept()

        # result_text = finder.driver.find_element(By.ID, "result")
        result_text = finder.visit_elem(By.ID, "result")
        print (result_text.text)
        break

    except TimeoutException:
        print("抓取超時：10 秒內沒看到目標元素")

    except NoSuchElementException:
        print("元素不存在")
        
    except Exception as e:
        print(f"其他未知錯誤: {e}")
else:
        print("已達到最大重試 3 次，抓取失敗。")


### 調整前，20260224 加上 retry 寫法 ###
# for i in range(3):
#     try:
#         alert_elem_1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Alert']")))
#         alert_elem_1.click()
#         alert_first = driver.switch_to.alert # 2. 將控制權切換到 Alert
#         print(f"警示框內容是: {alert_first.text}") # 3. 取得 Alert 上的文字內容
#         alert_first.accept() # 4. 點擊「確定」 (Accept)

#         alert_elem_2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Confirm']")))
#         alert_elem_2.click()
#         alert_second = driver.switch_to.alert
#         print(f"警示框內容是: {alert_second.text}")
#         alert_second.accept()

#         alert_elem_3 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Prompt']")))
#         alert_elem_3.click()
#         alert_third = driver.switch_to.alert
#         print(f"警示框內容是: {alert_third.text}")

#         # 輸入文字
#         alert_third.send_keys("My's Ryan")
#         alert_third.accept()

#         result_text = driver.find_element(By.ID, "result")
#         print (result_text.text)
#         driver.quit()
#         break

#     except TimeoutException:
#         print("抓取超時：10 秒內沒看到目標元素")
#         driver.switch_to.default_content()

#     except NoSuchElementException:
#         print("元素不存在")
#         driver.switch_to.default_content()
        
#     except Exception as e:
#         print(f"其他未知錯誤: {e}")
# else:
#         print("已達到最大重試 3 次，抓取失敗。")


## 調整前，最原始版本 ( 尚未優化 )
# alert1_elem = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Alert']")))
# alert1_elem.click()
# # driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click() # 1. 先點擊按鈕觸發 Alert
# # time.sleep(1)
# alert1 = driver.switch_to.alert # 2. 將控制權切換到 Alert
# print(f"警示框內容是: {alert1.text}") # 3. 取得 Alert 上的文字內容
# alert1.accept() # 4. 點擊「確定」 (Accept)

# alert2_elem = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Confirm']")))
# alert2_elem.click()
# # driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']").click()
# # time.sleep(1)
# alert2 = driver.switch_to.alert
# print(f"警示框內容是: {alert1.text}")
# alert2.accept()

# alert3_elem = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Prompt']")))
# alert3_elem.click()
# # driver.find_element(By.XPATH, "//button[text()='Click for JS Prompt']").click()
# # time.sleep(1)
# alert3 = driver.switch_to.alert
# print(f"警示框內容是: {alert1.text}")

# # 輸入文字
# alert3.send_keys("My's Ryan")
# alert3.accept()
# result_text = driver.find_element(By.ID, "result")
# print (result_text.text)
# driver.quit()