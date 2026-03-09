from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..", "..",".."))
sys.path.append(project_root)

from utils.drivers import WebController

finder = WebController()
finder.get_url("https://the-internet.herokuapp.com/iframe")

"""
2. IFrame 處理
    url = https://the-internet.herokuapp.com/iframe
    *target = print: id="tinymce"'s text (Your content goes here.)
    hint: iframe
"""
# 20260223 加上 retry 寫法
# 20260305 加上引用 drivers function，並調整 iframe 原本寫法(switch iframe) PR #6
# 20260307 刪除多餘註解 PR #7

for i in range(3):
    try:
        print(f"第 {i+1} 次抓取元素")
        
        # 切換 iframe 並尋找元素
        finder.wait_element_visible(By.ID, "mce_0_ifr")
        finder.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "mce_0_ifr")))
        input_form = finder.wait_element_visible(By.CSS_SELECTOR, ".mce-content-body p")
        
        print(f"抓取成功，輸出為 : {input_form.text}")
        
        break

    except TimeoutException:
        print("抓取超時：10 秒內沒看到目標元素")
        finder.iframe_switch()

    except NoSuchElementException:
        print("元素不存在")
        finder.iframe_switch()

    except Exception as e:
        print(f"其他未知錯誤: {e}")
        finder.iframe_switch() # 失敗也要記得切回主畫面再重試
else:
        print("已達到最大重試 3 次，抓取失敗。")