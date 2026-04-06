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

    def scan_high_gp_post(self):  # 取出巴哈文章標題
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

                    gp_value = 0
                    if gp_elem:
                        gp_text = gp_elem[0].text

                        if "爆" in gp_text:
                            gp_value = float("inf")

                        elif "爆" in gp_text:
                            titles.append(f"[{gp_text}] {title_elem.text}") # 20260405 跟下面>15的重複了
                        
                        elif gp_text == "" or gp_text == "0":
                            gp_value = 0
                        
                        else:
                            gp_value = int(gp_text)

                        # 取文章 gp 大於 15 的文章，並把標題存到 titles 裡
                        if gp_value > 15:
                            titles.append(f"[{gp_value}] {title_elem.text}")

                        # 比較目前的 (best_gp, best_art_elem) 與新的 (gp_value, title_elem)，取較大者同時更新兩個變數
                        best_gp, best_art_elem = max(
                            (best_gp, best_art_elem), (gp_value, title_elem))

                except Exception as e:
                    print(f"這樓跳過了，原因：{e}")  # 印出錯誤原因，但依然繼續跑下一輪
                    
        return titles, best_art_elem
    

    def scan_high_gp_content(self, choice): # 取出巴哈文章內回覆的 GP + 標題
        results = [] # 最終要回傳的內容清單
        page_best_gp = -1 # 記錄目前找到的最高 GP 數值（預設 -1）
        page_best_content = "無內容" # 對應最高 GP 的文章內容

        posts = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "section[id^='post_']")))

        for post in posts:
            gp_elements = post.find_elements(By.CSS_SELECTOR, ".postgp")

            if not gp_elements:
                print("此樓層找不到 GP 標籤，跳過")
                continue

            gp_text = gp_elements[0].text.strip()

            if "爆" in gp_text:
                # 爆文：直接取當前樓層內文
                try:
                    content = post.find_element(By.CSS_SELECTOR, ".c-article__content").text
                except:
                    content = "無法取得內文"

                if choice == "1":
                    results.append(content)
                    break  # 第一筆爆文就停止

                elif choice == "2":
                    results.append(content)  # 繼續找下一篇爆文

            else:
                # 一般文章：只更新 best，不 append
                clean_gp = "".join(filter(str.isdigit, gp_text))
                gp_value = int(clean_gp) if clean_gp else 0

                if gp_value > page_best_gp:
                    page_best_gp = gp_value

                    try:
                        page_best_content = post.find_element(By.CSS_SELECTOR, ".c-article__content").text
                    
                    except:
                        page_best_content = "無法取得內文"

        # 迴圈結束後，把 GP 最高的一般文章加進去
        if page_best_content != "無內容":
            results.append(page_best_content)

        return results # 結論 : ["爆文 A 的內容", "爆文 B 的內容", "GP 最高一般文的內容"])