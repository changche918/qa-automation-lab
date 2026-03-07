from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 20260305 加上 alert_switch、wait_elem function PR #6
class WebController:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10) # 先預設 10 秒

    def get_url(self, url):
        self.driver.get(url)

    def iframe_switch(self):
        """切回主頁面 default content"""
        self.driver.switch_to.default_content()

    def alert_switch(self):
        return self.driver.switch_to.alert # 這邊一定要記得 return 外面呼叫才能拿到東西
    
    def find_elem(self, elem_tuple):
        # 單純尋找並回傳元素
        return self.driver.find_element(*elem_tuple)

    def visit_elem(self, by_type, elem): # () >>> 傳遞 2 個參數 - 通常是 tuple，(()) >>> 只需要傳遞 1 個參數
        return self.wait.until(EC.visibility_of_element_located((by_type, elem)))
    
    def clickable_elem(self, by_type, elem):
        return self.wait.until(EC.element_to_be_clickable((by_type, elem)))

    
    
