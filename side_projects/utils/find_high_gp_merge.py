from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class FindHighGP:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def scan_high_gp(self, mode, choice=None):
        """
        mode="post"    : 掃描文章列表頁，回傳 GP > 15 的文章標題
        mode="content" : 掃描文章內回覆，回傳高 GP 樓層內文
        choice (mode="content" 專用): "1" 遇到第一筆爆文就停止，"2" 收集所有爆文
        """
        results = []
        page_best_gp = -1
        page_best_item = None  # post 模式存 title element；content 模式存內文字串

        # 依模式選擇等待的元素
        selector = ".b-list__row.b-list-item" if mode == "post" else "section[id^='post_']"
        items = self.wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, selector))
        )

        for item in items:
            # post 模式：排除置頂文
            if mode == "post" and "b-list__row--sticky" in item.get_attribute("class"):
                continue

            try:
                gp_css = ".b-list__summary__gp.b-gp" if mode == "post" else ".postgp"
                gp_elements = item.find_elements(By.CSS_SELECTOR, gp_css)
                if not gp_elements:
                    print("此樓層找不到 GP 標籤，跳過")
                    continue

                gp_text = gp_elements[0].text.strip()

                if "爆" in gp_text:
                    gp_value = float("inf")
                    if mode == "content":  # 爆文：直接取當前樓層內文
                        content = item.find_element(By.CSS_SELECTOR, ".c-article__content").text
                        results.append(f"[{gp_text}] {content}")
                        if choice == "1":
                            break  # 第一筆爆文就停止
                        continue  # choice == "2"：繼續找下一筆，不進 best 比較
                else:
                    clean_gp = "".join(filter(str.isdigit, gp_text))
                    gp_value = int(clean_gp) if clean_gp else 0

                if mode == "post":
                    title_elem = item.find_element(By.CSS_SELECTOR, ".b-list__main__title")
                    if gp_value > 15:  # 爆文（inf > 15）也能被收錄
                        results.append(f"[{gp_value}] {title_elem.text}")
                    if gp_value > page_best_gp:
                        page_best_gp = gp_value
                        page_best_item = title_elem
                else:
                    if gp_value > page_best_gp:
                        page_best_gp = gp_value
                        page_best_item = item.find_element(
                            By.CSS_SELECTOR, ".c-article__content"
                        ).text

            except Exception as e:
                print(f"這樓跳過了，原因：{e}")  # 印出錯誤原因，但依然繼續跑下一輪

        # 迴圈結束後，把本頁 GP 最高的一般項目加進去
        if page_best_item:
            if mode == "post":
                results.append(f"[{page_best_gp}] {page_best_item.text}")
            else:
                results.append(f"[{page_best_gp}] {page_best_item}")

        return results  # 結論：["爆文 A 的內容", "爆文 B 的內容", "GP 最高一般文的內容"]
