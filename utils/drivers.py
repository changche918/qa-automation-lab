from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


# 20260305 加上 alert_switch、wait_elem function PR #6
# 20260307 改寫 function，以及加上 function 說法 PR #7
class WebController:
    def __init__(self):
        # self.options = Options()  # 設定瀏覽器選項
        # self.options.add_argument("--headless=new")  # 開啟「無頭模式」 (Headless Mode)
        # self.driver = WebDriver.Chrome(options=self.options)
        # self.wait = WebDriverWait(self.driver, 10)
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_url(self, url):
        """前往指定的網頁網址。
        Args:
            url: 目標網頁的完整網址 (URL)，必須包含 http 或 https。
        """
        self.driver.get(url)

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
