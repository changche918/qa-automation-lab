from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException 
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..", "..",".."))
sys.path.append(project_root)

from utils.drivers import WebController

finder = WebController()
finder.get_url("https://the-internet.herokuapp.com/hovers")

"""
## 基礎練習 ##
1. Hovers
    url = "https://the-internet.herokuapp.com/hovers"
    *target = hover user1 and click "View Profile"
    hint: Hovers

2/22 確認hovers為何錯誤    
"""
# 20260223 加上 retry 寫法
# 20260305 加上引用 drivers function，並調整 hovers 原本寫法 PR #6
# 20260307 調整變數名稱，刪除多餘註解 PR #7

for i in range(3):
    try:
        print(f"第 {i+1} 次抓取元素")
        # 1. 定位「滑鼠要移上去」的那個容器（通常是頭像圖片）
        hover_target = finder.wait_element_visible(By.CLASS_NAME, "figure") # 要 hover 的對象

        # 2. 執行懸停動作
        actions = ActionChains(finder.driver)
        actions.move_to_element(hover_target).perform()

        # 3. 等待文字出現
        user_name_element = finder.wait_element_visible(By.CSS_SELECTOR, ".figcaption h5")

        # 4. 取得文字 name 1 + 點擊下方的 view profile
        view_profile_text = finder.wait_element_visible(By.LINK_TEXT, "View profile")

        if view_profile_text.text == 'View profile':
            view_profile_text.click()
            new_page = finder.wait_element_visible(By.TAG_NAME, "h1")
            if new_page.text == "Not Found": # 這邊需要完整比對 Not Found 字串
                print("已成功進入 Not Found 頁面")
            break     

    except TimeoutException:
        print("抓取超時：10 秒內沒看到目標元素")
    
    except NoSuchElementException:
        print("元素不存在")

    except Exception as e:
        print(f"其他未知錯誤: {e}")
else:
        print("已達到最大重試 3 次，抓取失敗。")