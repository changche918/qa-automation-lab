from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException


driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/iframe")
"""
2. IFrame 處理
    url = https://the-internet.herokuapp.com/iframe
    *target = print: id="tinymce"'s text (Your content goes here.)
    hint: iframe
"""
wait = WebDriverWait(driver, 10)

# # 等待 iframe 出現並自動切換進去
# WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "mce_0_ifr")))

# # 現在已經在 iframe 裡面了，直接操作
# input_form = wait.until(
#     EC.visibility_of_element_located((By.CSS_SELECTOR, ".mce-content-body.mce-content-readonly p")))
# print(input_form.text)
# driver.switch_to.default_content()



# 20260224 加上 retry 寫法
for i in range(3):
    try:
        print(f"第 {i+1} 次抓取元素")
        
        # 切換 iframe 並尋找元素
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "mce_0_ifr")))
        input_form = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".mce-content-body p")))
        
        print(f"抓取成功，輸出為 : {input_form.text}")
        break

    except TimeoutException:
        print("抓取超時：10 秒內沒看到目標元素")
        driver.switch_to.default_content()

    except NoSuchElementException:
        print("元素不存在")
        driver.switch_to.default_content()

    except Exception as e:
        print(f"其他未知錯誤: {e}")
        driver.switch_to.default_content() # 失敗也要記得切回主畫面再重試
else:
        print("已達到最大重試 3 次，抓取失敗。")