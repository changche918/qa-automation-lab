from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

# 20260305 加上 alert_switch、wait_elem function PR #6
# 20260307 改寫 function，以及加上 function 說法 PR #7
class WebController:
    def __init__(self):
        self.options = Options() # 設定瀏覽器選項
        self.options.add_argument("--headless=new") # 開啟「無頭模式」 (Headless Mode)
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 10)

    def get_url(self, url):
        self.driver.get(url)

    def iframe_switch(self):
        """切回主頁面 default content"""
        self.driver.switch_to.default_content()
    
    def wait_alert(self, timeout=10):
        """等待並捕捉瀏覽器彈出的警示框 (Alert)。
        Args:
            timeout (int): 最長等待秒數，預設為 10 秒。
        Returns:
            Alert: 返回 Selenium 的 Alert 物件，可用於 .text 讀取文字或 .accept() 點擊確定。
        """
        return WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
    
    def find_elem(self, by_type, elem_str):
        return self.driver.find_element(by_type, elem_str)

    def wait_element_visible(self, by_type, elem):
        return self.wait.until(EC.visibility_of_element_located((by_type, elem)))
    
    def clickable_elem(self, by_type, elem):
        return self.wait.until(EC.element_to_be_clickable((by_type, elem)))

    
    
