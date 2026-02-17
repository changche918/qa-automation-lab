from selenium import webdriver

# class driver:
#     def __init__ (self, browser_name):
#         self.browser_name = browser_name
#     def driver_type(self):
#         aaa = webdriver.self.browser_name()
#         aaa.get("https://www.104.com.tw/")


from selenium import webdriver

class Browser:
    def __init__(self, browser_name):
        # 確保傳入名稱正確 (如: "Chrome", "Firefox")
        self.browser_name = browser_name.capitalize()
        self.driver = None

    def start_service(self):
        """僅負責啟動瀏覽器實例"""
        driver_class = getattr(webdriver, self.browser_name)
        self.driver = driver_class()
        print(f"系統訊息：{self.browser_name} 已啟動。")


    def open_page(self, url):
        """
        這就是你要的功能：讓網址成為參數。
        傳入任何網址，它就會跳轉。
        """
        if self.driver:
            print(f"正在前往：{url}")
            self.driver.get(url)
        else:
            print("錯誤：瀏覽器尚未啟動，請先執行 start_service()")

        self.driver.quit()