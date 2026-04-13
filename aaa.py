from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class FindHighGP:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        
    def scan_high_gp_post(self):  # 取出巴哈文章標題
        high_gp_post_titles = []
        page_best_gp = -1  # 文章最少是 0，所以初始值給 -1 來比大小
        best_art_titles = None

        # 抓文章列表頁
        articles = self.wait.until(
            EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, ".b-list__row.b-list-item")
            )
        )

        for art in articles:  # articles = 文章清單，art = 每篇文章
            if "b-list__row--sticky" not in art.get_attribute("class"):  # 排除置頂文
                try:
                    title_elem = art.find_element(
                        By.CSS_SELECTOR, ".b-list__main__title"
                    )
                    gp_elements = art.find_elements(
                        By.CSS_SELECTOR, ".b-list__summary__gp.b-gp"
                    )
                    if not gp_elements:
                        print("此樓層找不到 GP 標籤，跳過")
                        continue

                    gp_text = gp_elements[0].text.strip()

                    if "爆" in gp_text:
                        gp_value = float("inf")
                    elif gp_text == "" or gp_text == "0":
                        gp_value = 0
                    else:
                        gp_value = int(gp_text)

                    # 取文章 gp 大於 15 的文章，並把標題存到 titles 裡
                    if gp_value > 15:  # ✏ 移出 else，爆文（inf > 15）也能被收錄
                        high_gp_post_titles.append(f"[{gp_value}] {title_elem.text}")

                    if gp_value > page_best_gp:  # ✏ 同上，移出 else
                        page_best_gp = gp_value
                        best_art_titles = title_elem

                except Exception as e:
                    print(f"這樓跳過了，原因：{e}")  # 印出錯誤原因，但依然繼續跑下一輪

        # return high_gp_post_titles, best_art_titles
        if best_art_titles:
            high_gp_post_titles.append(f"[{page_best_gp}] {best_art_titles.text}")  # ✏ 補 .text
        return (high_gp_post_titles)  # 結論 : ["爆文 A 的內容", "爆文 B 的內容", "GP 最高一般文的內容"])
        