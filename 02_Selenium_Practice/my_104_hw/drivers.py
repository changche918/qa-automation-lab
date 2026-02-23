from selenium import webdriver

class WebController:
    def __init__(self):
        self.driver = webdriver.Chrome()
    def get_url(self, url):
        self.driver.get(url)
    def find_elem(self, elem_tuple):
        # 單純尋找並回傳元素
        return self.driver.find_element(*elem_tuple)

