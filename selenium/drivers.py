from selenium import webdriver

# class driver:
#     def __init__ (self, browser_name):
#         self.browser_name = browser_name
#     def driver_type(self):
#         aaa = webdriver.self.browser_name()
#         aaa.get("https://www.104.com.tw/")

# class s:
#     def __init__(self):
#         pass
#     def init_browser(url, elem):
#         driver = webdriver.Chrome()
#         driver.get(url)
#         driver.find_element(elem)
#         # return driver # 關鍵：把控制權傳回去

class ElementFinder:
    def __init__(self):
        self.driver = webdriver.Chrome()
    def get_url(self, url):
        self.driver.get(url)
    def find_elem(self, elem_tuple):
        # 單純尋找並回傳元素
        return self.driver.find_element(*elem_tuple)

