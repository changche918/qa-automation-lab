from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 20260324 新增 function PR #10
# 20260326 調整程式寫法，將 log.save 移出去處理，並繼承 driver 寫法 PR #11
# 20260402 增加 function，區分撈第一筆及所有爆文章 PR #12
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
                    gp_value = float("inf")
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
    
    # def scan_high_gp_post(self):
    def scan_first_high_gp_post(self):
        titles = []
        best_gp = -1  # 文章最少是 0，所以初始值給 -1 來比大小
        best_art_elem = None

        # 抓文章列表頁
        articles = self.wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".b-list__row.b-list-item"))
        )

        for art in articles:  # articles = 文章清單，art = 每篇文章
            if "b-list__row--sticky" not in art.get_attribute("class"):  # 排除置頂文
                try:
                    title_elem = art.find_element(By.CSS_SELECTOR, ".b-list__main__title")
                    gp_elem = art.find_elements(By.CSS_SELECTOR, ".b-list__summary__gp.b-gp")

                    if gp_elem:
                        gp_text = gp_elem[0].text
                        if "爆" in gp_text:
                            gp_value = float("inf")
                        elif gp_text == "" or gp_text == "0":
                            gp_value = 0
                        else:
                            gp_value = int(gp_text)

                        # 文章 GP 比大小，印出超過 15 的
                        # 用前面語法將 gp_text 轉成 gp_value，best_gp 是初始設定 -1，之後會被新的 gp_value 取代
                        # if gp_value > 15:
                        #     titles.append(f"[{gp_value}] {title_elem.text}")
                        #     if gp_value > best_gp:
                        #         best_gp = gp_value
                        #         best_art_elem = title_elem

                        # 另一種寫法比大小寫法
                        if gp_value > 15:
                            titles.append(f"[{gp_value}] {title_elem.text}")

                        # 比較目前的 (best_gp, best_art_elem) 與新的 (gp_value, title_elem)
                        # 取較大者並同時更新兩個變數
                        best_gp, best_art_elem = max(
                            (best_gp, best_art_elem), (gp_value, title_elem)
                        )

                except Exception as e:
                    print(f"這樓跳過了，原因：{e}")  # 印出錯誤原因，但依然繼續跑下一輪
        return titles, best_art_elem
    
    def scan_each_high_gp_post(self):
        titles = []
        best_gp = -1  # 文章最少是 0，所以初始值給 -1 來比大小
        best_art_elem = None

        articles = self.wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".b-list__row.b-list-item"))
        )

        for art in articles:
            if "b-list__row--sticky" not in art.get_attribute("class"):
                try:
                    title_elem = art.find_element(By.CSS_SELECTOR, ".b-list__main__title")
                    gp_elem = art.find_elements(By.CSS_SELECTOR, ".b-list__summary__gp.b-gp")

                    if gp_elem:
                        gp_text = gp_elem[0].text
                        if "爆" in gp_text:
                            titles.append(f"[{gp_text}] {title_elem.text}")
                        elif gp_text == "" or gp_text == "0":
                            gp_value = 0
                        else:
                            gp_value = int(gp_text)

                        if gp_value > 15:
                            titles.append(f"[{gp_value}] {title_elem.text}")

                        best_gp, best_art_elem = max(
                            (best_gp, best_art_elem), (gp_value, title_elem)
                        )

                except Exception as e:
                    print(f"這樓跳過了，原因：{e}")
        return titles, best_art_elem
    

