    

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
    
class FindHighGP:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        
    def scan_high_gp_content(self, choice):  # 取出巴哈文章內回覆的 GP + 標題
        high_gp_content = []  # 最終要回傳的內容清單
        page_best_gp = -1  # 記錄目前找到的最高 GP 數值（預設 -1）
        page_best_content = None  # 對應最高 GP 的文章內容

        # 抓回覆文列表
        posts = self.wait.until(
            EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, "section[id^='post_']")
            )
        )

        for post in posts:
            try:
                gp_elements = post.find_elements(By.CSS_SELECTOR, ".postgp")
                if not gp_elements:
                    print("此樓層找不到 GP 標籤，跳過")
                    continue

                gp_text = gp_elements[0].text.strip()

                if "爆" in gp_text:  # 爆文：直接取當前樓層內文
                    content = post.find_element(By.CSS_SELECTOR, ".c-article__content").text  # ✏ 取當前樓內文，不用可能是 None 的 page_best_content
                    if choice == "1":
                        high_gp_content.append(f"[{gp_text}] {content}")
                        break  # 第一筆爆文就停止
                    elif choice == "2":
                        high_gp_content.append(f"[{gp_text}] {content}")  # 繼續找下一篇爆文

                else:
                    # 一般文章：只更新 best，不 append
                    clean_gp = "".join(
                        filter(str.isdigit, gp_text)
                    )  # 過濾成數字下面比較好比較
                    if clean_gp:
                        # 如果 clean_gp 不是空字串，就轉換成整數
                        gp_value = int(clean_gp)
                    else:
                        # 如果 clean_gp 是空字串（代表沒抓到數字），就設為 0
                        gp_value = 0

                    if gp_value > page_best_gp:
                        page_best_gp = gp_value
                        page_best_content = post.find_element(
                            By.CSS_SELECTOR, ".c-article__content").text  # ✏ 修正縮排

            except Exception as e:
                print(f"這樓跳過了，原因：{e}")  # 印出錯誤原因，但依然繼續跑下一輪

        # 迴圈結束後，把 GP 最高的一般文章加進去
        if page_best_content:
            high_gp_content.append(f"[{page_best_gp}] {page_best_content}")
        return (
            high_gp_content  # 結論 : ["爆文 A 的內容", "爆文 B 的內容", "GP 最高一般文的內容"])
        )