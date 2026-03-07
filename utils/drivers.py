from selenium import webdriver

# 20260305 加上 alert_switch function PR #?

class WebController:
    def __init__(self):
        self.driver = webdriver.Chrome()
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
    
    
