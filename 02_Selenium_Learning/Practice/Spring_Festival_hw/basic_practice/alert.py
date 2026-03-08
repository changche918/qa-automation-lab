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
# 20260307 調整變數名稱，刪除多餘註解 PR #7

for i in range(3):
    try:
        alert_elem = finder.wait_element_visible(By.XPATH, "//button[text()='Click for JS Alert']")
        confirm_elem = finder.wait_element_visible(By.XPATH, "//button[text()='Click for JS Confirm']")
        prompt_elem = finder.wait_element_visible(By.XPATH, "//button[text()='Click for JS Prompt']")

        javascript_alerts = [alert_elem, confirm_elem, prompt_elem]
        
        for button in javascript_alerts:
            button.click()
            alert_title = finder.wait_alert()
            print(f"警示框內容是 : {alert_title.text}")
            alert_title.accept()

        prompt_elem.click() # 只對 prompt alert 做操作
        alert_box = finder.wait_alert()
        alert_box.send_keys("My's Ryan")
        alert_box.accept()

        result_text = finder.wait_element_visible(By.ID, "result")
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