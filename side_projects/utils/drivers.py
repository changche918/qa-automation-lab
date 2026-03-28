from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class WebController():
    def __init__(self):
        # 1. 先設定 Options (選項)
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('--headless') # 視需求開啟
        
        # 2. 啟動瀏覽器 (將 options 傳入)
        self.driver = webdriver.Chrome(options=self.options)
        
        # 3. 瀏覽器啟動後，才能執行視窗操作與設定等待
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def get_url(self, url):
        """前往指定的網頁網址。
        Args:
            url: 目標網頁的完整網址 (URL)，必須包含 http 或 https。
        """
        self.driver.get(url)

    def get_current_url(self):
        return self.driver.current_url

    def iframe_switch(self):
        """切回主頁面 default content"""
        self.driver.switch_to.default_content()

    def wait_alert(self, timeout=10):
        """等待並捕捉瀏覽器彈出的警示框 (Alert)。
        Args:
            timeout: 最長等待秒數，預設為 10 秒。
        """
        return WebDriverWait(self.driver, timeout).until(EC.alert_is_present())

    def wait_element_visible(self, by_type, elem):
        """等待尋找的元素可見後再尋找。
        Args:
            傳入需要等待什麼元素出現 e.g. wait_element_visible(By.CSS_SELECTOR, "my-paragraph")
        """
        return self.wait.until(EC.visibility_of_element_located((by_type, elem)))

    def wait_element_clickable(self, by_type, elem):
        """等待尋找的元素可以點擊後才點擊。
        Args:
            傳入需要等待什麼元素可點擊 e.g. wait_element_clickable(By.CSS_SELECTOR, "my-paragraph")
        """
        return self.wait.until(EC.element_to_be_clickable((by_type, elem)))
    
    def find_element(self, by_type, elem):
        return self.driver.find_element(by_type, elem)

    def find_elements(self, by_type, elem):
        return self.driver.find_elements(by_type, elem)
    
    def close_windows(self):
        self.driver.quit()