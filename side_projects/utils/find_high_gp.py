from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 20260324 新增 function PR #10
# 20260326 調整程式寫法，將 log.save 移出去處理，並繼承 driver 寫法 PR #11
class FindHighGP():
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def scan_high_gp_content(self):
        results = []
        page_best_gp = -1 # 文章最少是 0，所以初始值給 -1 來比大小
        page_best_content = "無內容"

        # 1. 確保這頁樓層載入
        posts = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "section[id^='post_']")))

        # 2. 掃描本頁所有樓層
        for post in posts:
            gp_elements = post.find_elements(By.CSS_SELECTOR, ".postgp")
            
            if gp_elements:
                gp_text = gp_elements[0].text.strip() # 先抓大範圍，再從大範圍裡抓小東西

                if "爆" in gp_text:
                    gp_value = 99999
                else:
                    # 只保留數字，過濾掉非數字字元
                    clean_gp = "".join(filter(str.isdigit, gp_text)) # TODO 待理解
                    gp_value = int(clean_gp) if clean_gp else 0 # TODO 待理解

                    if gp_value > page_best_gp:
                        page_best_gp = gp_value
                        try:
                            page_best_content = post.find_element(By.CSS_SELECTOR, ".c-article__content").text
                            results.append(page_best_content)
                        except:
                            page_best_content = "無法取得內文"
                            
            else:
                print("此樓層找不到 GP 標籤，跳過")

        return results