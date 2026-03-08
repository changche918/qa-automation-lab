from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..", "..",".."))
sys.path.append(project_root)

from utils.drivers import WebController

finder = WebController()
finder.get_url("https://the-internet.herokuapp.com/shadowdom")
# wait = WebDriverWait(finder.driver, 10)

""""
4. shadow-root
    url = https://the-internet.herokuapp.com/shadowdom
    *target = print: name="my-text"'s text (My default text)
    hint: shadow-root
"""
# 20260223 加上 retry 寫法
# 20260305 加上引用 drivers function，並調整 shadow 原本寫法 PR #6

for i in range(3):
    try:
        print(f"第 {i+1} 次抓取元素")
        
        # 1. 找到宿主元素 (Host)
        # host = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "my-paragraph")))
        host = finder.visit_elem(By.CSS_SELECTOR, "my-paragraph")
        
        # 2. 取得 shadow_root
        root = host.shadow_root
        
        # 3. 在 shadow_root 內部尋找元素
        # inner_p = root.find_element(By.CSS_SELECTOR, "slot")

        # 如果要將 line 31 改成 EC 寫法要改成這樣 :
        # inner_p = finder.wait_elem(lambda _: root.find_element(By.CSS_SELECTOR, "slot"))
        
        '''這邊套用 function = visit_elem 後不正確，待解決 
        inner_p = finder.visit_elem(By.CSS_SELECTOR, "slot")

        print(f"抓取成功，輸出為 : {inner_p.text}")
        break
        '''
    except TimeoutException:
        print("抓取超時：10 秒內沒看到目標元素")

    except NoSuchElementException:
        print("元素不存在")

    except Exception as e:
        print(f"其他未知錯誤: {e}")
else:
        print("已達到最大重試 3 次，抓取失敗。")

# # 1. 找到宿主元素 (Host)
# host = driver.find_element(By.CSS_SELECTOR, "my-paragraph")

# # 2. 取得 shadow_root
# root = host.shadow_root

# # 3. 在 shadow_root 內部尋找元素
# inner_p = root.find_element(By.CSS_SELECTOR, "slot")
# print(inner_p.text)