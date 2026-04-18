from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# 20260324 新增 function PR #10
# 20260326 調整程式寫法，將 log.save 移出去處理，並繼承 driver 寫法 PR #11
# 20260402 增加 function，區分撈第一筆及所有爆文章 PR #12
# 20260407 新增合併 function 練習 PR #12
class FindHighGP:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

#     def scan_high_gp_post_原來(self):  # 取出巴哈文章標題
#         titles = []
#         best_gp = -1  # 文章最少是 0，所以初始值給 -1 來比大小
#         best_art_elem = None

#         # 抓文章列表頁
#         articles = self.wait.until(
#             EC.visibility_of_all_elements_located(
#                 (By.CSS_SELECTOR, ".b-list__row.b-list-item")
#             )
#         )

#         for art in articles:  # articles = 文章清單，art = 每篇文章
#             if "b-list__row--sticky" not in art.get_attribute("class"):  # 排除置頂文
#                 try:
#                     title_elem = art.find_element(
#                         By.CSS_SELECTOR, ".b-list__main__title"
#                     )
#                     gp_elem = art.find_elements(
#                         By.CSS_SELECTOR, ".b-list__summary__gp.b-gp"
#                     )

#                     gp_value = 0
#                     if gp_elem:
#                         gp_text = gp_elem[0].text
#                         if "爆" in gp_text:
#                             gp_value = float("inf")
#                         elif gp_text == "" or gp_text == "0":
#                             gp_value = 0
#                         else:
#                             gp_value = int(gp_text)

#                         # 取文章 gp 大於 15 的文章，並把標題存到 titles 裡
#                         if gp_value > 15:
#                             titles.append(f"[{gp_value}] {title_elem.text}")
#                         if gp_value > best_gp:
#                             best_gp = gp_value
#                             best_art_elem = title_elem
#                 except Exception as e:
#                     print(f"這樓跳過了，原因：{e}")  # 印出錯誤原因，但依然繼續跑下一輪

#         return titles, best_art_elem

#     def scan_high_gp_content(self, choice):  # 取出巴哈文章內回覆的 GP + 標題
#         results = []  # 最終要回傳的內容清單
#         page_best_gp = -1  # 記錄目前找到的最高 GP 數值（預設 -1）
#         page_best_content = None  # 對應最高 GP 的文章內容

#         posts = self.wait.until(
#             EC.presence_of_all_elements_located(
#                 (By.CSS_SELECTOR, "section[id^='post_']")
#             )
#         )

#         for post in posts:
#             gp_elements = post.find_elements(By.CSS_SELECTOR, ".postgp")
#             if not gp_elements:
#                 print("此樓層找不到 GP 標籤，跳過")
#                 continue
#             gp_text = gp_elements[0].text.strip()
#             if "爆" in gp_text:  # 爆文：直接取當前樓層內文
#                 try:
#                     content = post.find_element(
#                         By.CSS_SELECTOR, ".c-article__content"
#                     ).text
#                 except:
#                     content = "無法取得內文"
#                 if choice == "1":
#                     results.append(f"[{gp_text}] {content}")
#                     break  # 第一筆爆文就停止
#                 elif choice == "2":
#                     results.append(f"[{gp_text}] {content}")  # 繼續找下一篇爆文

#             else:
#                 # 一般文章：只更新 best，不 append
#                 clean_gp = "".join(
#                     filter(str.isdigit, gp_text)
#                 )  # 過濾成數字下面比較好比較
#                 if clean_gp:
#                     # 如果 clean_gp 不是空字串，就轉換成整數
#                     gp_value = int(clean_gp)
#                 else:
#                     # 如果 clean_gp 是空字串（代表沒抓到數字），就設為 0
#                     gp_value = 0

#                 if gp_value > page_best_gp:
#                     page_best_gp = gp_value
#                     try:
#                         page_best_content = post.find_element(
#                             By.CSS_SELECTOR, ".c-article__content"
#                         ).text
#                     except:
#                         page_best_content = "無法取得內文"

#         # 迴圈結束後，把 GP 最高的一般文章加進去
#         if page_best_content:
#             results.append(f"[{page_best_gp}] {page_best_content}")
#         return (
#             results  # 結論 : ["爆文 A 的內容", "爆文 B 的內容", "GP 最高一般文的內容"])
#         )


# ########################### AI 合併 function ###########################
    
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
                    gp_css = ".b-list__summary__gp.b-gp" # 文章的 GP
                else:
                    gp_css = ".postgp" # 回覆文的 GP

                # 在當前項目內尋找 GP 元素（回傳清單）
                gp_elements = item.find_elements(By.CSS_SELECTOR, gp_css)

                # 若找不到 GP 元素，印出提示並跳過此項目
                if not gp_elements:
                    print("此樓層找不到 GP 標籤，跳過")
                    continue

                # 取第一個 GP 元素的文字，並去除前後空白
                gp_text = gp_elements[0].text.strip()

                # 判斷 GP 是否為「爆」（ PTT 規則：推文數超過 100 顯示「爆」）
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
   
    
########################### ### 以下為未改前的版本 ### ###########################
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
        return (
            high_gp_post_titles  # 結論 : ["爆文 A 的內容", "爆文 B 的內容", "GP 最高一般文的內容"])
        )


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
