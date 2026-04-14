# 從 selenium 套件匯入定位元素的方式（By.CSS_SELECTOR 等）
from selenium.webdriver.common.by import By
# 匯入等待條件模組，用來判斷元素是否出現在頁面上
from selenium.webdriver.support import expected_conditions as EC
# 匯入顯式等待工具，可以設定最長等待秒數
from selenium.webdriver.support.ui import WebDriverWait

class FindHighGP:
    def __init__(self, driver):
        # 儲存瀏覽器驅動物件，供類別內其他方法使用
        self.driver = driver
        # 建立顯式等待物件，最多等待 10 秒讓元素出現
        self.wait = WebDriverWait(self.driver, 10)

    def scan_high_gp(self, mode, choice=None):
        """
        mode="post"    : 掃描文章列表頁，回傳 GP > 15 的文章標題
        mode="content" : 掃描文章內回覆，回傳高 GP 樓層內文
        choice (mode="content" 專用): "1" 遇到第一筆爆文就停止，"2" 收集所有爆文
        """
        # 初始化結果清單，用來收集符合條件的文章或樓層
        results = []
        # 記錄本頁目前找到的最高 GP 數值，初始設為 -1 表示尚未找到任何項目
        page_best_gp = -1
        # 記錄本頁 GP 最高的項目：post 模式存 title element；content 模式存內文字串
        page_best_item = None

        # 依照模式選擇對應的 CSS 選擇器：
        # post 模式 → 文章列表的每一列；content 模式 → 文章內以 "post_" 開頭 id 的 section（每一樓）
        
        if mode == "post":
            selector = ".b-list__row.b-list-item" 
        else:
            selector = "section[id^='post_']"

        # 等待頁面上符合選擇器的所有元素都出現（可見），並取得元素清單
        items = self.wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, selector))
        )

        # 逐一處理每個文章列或樓層
        for item in items:
            # post 模式專用：若該列有置頂樣式，代表是置頂文，略過不計入統計
            if mode == "post" and "b-list__row--sticky" in item.get_attribute("class"):
                continue

            try:
                # 依照模式選擇對應的 GP 數字元素 CSS 選擇器
                if mode == "post": 
                    gp_css = ".b-list__summary__gp.b-gp"
                else:
                    gp_css = ".postgp"

                # 在當前項目內尋找 GP 元素（回傳清單）
                gp_elements = item.find_elements(By.CSS_SELECTOR, gp_css)

                # 若找不到 GP 元素，印出提示並跳過此項目
                if not gp_elements:
                    print("此樓層找不到 GP 標籤，跳過")
                    continue

                # 取第一個 GP 元素的文字，並去除前後空白
                gp_text = gp_elements[0].text.strip()

                # 判斷 GP 是否為「爆」（PTT 規則：推文數超過 100 顯示「爆」）
                if "爆" in gp_text:
                    # 爆文的 GP 視為無限大，確保一定比任何數值都高
                    gp_value = float("inf")

                    if mode == "content":
                        # content 模式：取得該樓層的內文文字
                        content = item.find_element(By.CSS_SELECTOR, ".c-article__content").text
                        # 將爆文內文加入結果清單，格式：[爆] 內文
                        results.append(f"[{gp_text}] {content}")

                        if choice == "1":
                            # 使用者選擇只要第一筆爆文，找到後立即停止迴圈
                            break
                        # choice == "2"：繼續往下找其他爆文，不進行 best 比較
                        continue
                else:
                    # 非爆文：從 GP 文字中只保留數字字元（過濾掉 X 或其他符號）
                    clean_gp = "".join(filter(str.isdigit, gp_text))
                    # 若有數字則轉為整數，否則設為 0（代表無推文或被噓）
                    gp_value = int(clean_gp) if clean_gp else 0

                if mode == "post":
                    # post 模式：取得該列的文章標題元素
                    title_elem = item.find_element(By.CSS_SELECTOR, ".b-list__main__title")

                    # 若 GP > 15（爆文的 inf 也符合），將標題加入結果清單
                    if gp_value > 15:
                        results.append(f"[{gp_value}] {title_elem.text}")

                    # 更新本頁最高 GP 記錄（用於迴圈結束後補上最高分項目）
                    if gp_value > page_best_gp:
                        page_best_gp = gp_value
                        page_best_item = title_elem  # 儲存標題元素以供後續取文字
                else:
                    # content 模式（非爆文）：更新本頁最高 GP 記錄
                    if gp_value > page_best_gp:
                        page_best_gp = gp_value
                        # 直接儲存內文字串（而非元素），避免後續元素失效
                        page_best_item = item.find_element(
                            By.CSS_SELECTOR, ".c-article__content"
                        ).text

            except Exception as e:
                # 若某個項目處理時發生錯誤（例如元素不存在），印出原因並繼續下一個項目
                print(f"這樓跳過了，原因：{e}")

        # 迴圈結束後，將本頁 GP 最高的一般項目（非爆文）補充加入結果清單
        if page_best_item:
            if mode == "post":
                # post 模式：從標題元素取出文字
                results.append(f"[{page_best_gp}] {page_best_item.text}")
            else:
                # content 模式：page_best_item 已是字串，直接使用
                results.append(f"[{page_best_gp}] {page_best_item}")

        # 回傳結果清單，例如：["[爆] 爆文A內容", "[爆] 爆文B內容", "[35] GP最高一般文內容"]
        return results
