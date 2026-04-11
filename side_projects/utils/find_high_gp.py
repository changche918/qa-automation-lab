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

    """
    def scan_high_gp_post_原來(self):  # 取出巴哈文章標題
        titles = []
        best_gp = -1  # 文章最少是 0，所以初始值給 -1 來比大小
        best_art_elem = None

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
                    gp_elem = art.find_elements(
                        By.CSS_SELECTOR, ".b-list__summary__gp.b-gp"
                    )

                    gp_value = 0
                    if gp_elem:
                        gp_text = gp_elem[0].text
                        if "爆" in gp_text:
                            gp_value = float("inf")
                        elif gp_text == "" or gp_text == "0":
                            gp_value = 0
                        else:
                            gp_value = int(gp_text)

                        # 取文章 gp 大於 15 的文章，並把標題存到 titles 裡
                        if gp_value > 15:
                            titles.append(f"[{gp_value}] {title_elem.text}")
                        if gp_value > best_gp:
                            best_gp = gp_value
                            best_art_elem = title_elem
                except Exception as e:
                    print(f"這樓跳過了，原因：{e}")  # 印出錯誤原因，但依然繼續跑下一輪

        return titles, best_art_elem

    def scan_high_gp_content(self, choice):  # 取出巴哈文章內回覆的 GP + 標題
        results = []  # 最終要回傳的內容清單
        page_best_gp = -1  # 記錄目前找到的最高 GP 數值（預設 -1）
        page_best_content = None  # 對應最高 GP 的文章內容

        posts = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "section[id^='post_']")
            )
        )

        for post in posts:
            gp_elements = post.find_elements(By.CSS_SELECTOR, ".postgp")
            if not gp_elements:
                print("此樓層找不到 GP 標籤，跳過")
                continue
            gp_text = gp_elements[0].text.strip()
            if "爆" in gp_text:  # 爆文：直接取當前樓層內文
                try:
                    content = post.find_element(
                        By.CSS_SELECTOR, ".c-article__content"
                    ).text
                except:
                    content = "無法取得內文"
                if choice == "1":
                    results.append(f"[{gp_text}] {content}")
                    break  # 第一筆爆文就停止
                elif choice == "2":
                    results.append(f"[{gp_text}] {content}")  # 繼續找下一篇爆文

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
                    try:
                        page_best_content = post.find_element(
                            By.CSS_SELECTOR, ".c-article__content"
                        ).text
                    except:
                        page_best_content = "無法取得內文"

        # 迴圈結束後，把 GP 最高的一般文章加進去
        if page_best_content:
            results.append(f"[{page_best_gp}] {page_best_content}")
        return (
            results  # 結論 : ["爆文 A 的內容", "爆文 B 的內容", "GP 最高一般文的內容"])
        )
    """

########################### 嘗試合併 function ###########################

    
    def scan_high_gp_post(self):
        high_gp_post_titles = []
        page_best_gp = -1
        best_art_titles = None

        articles = self.wait.until(
            EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, ".b-list__row.b-list-item")
            )
        )

        for art in articles:
            if "b-list__row--sticky" not in art.get_attribute("class"):
                try:
                    title_elem = art.find_element(
                        By.CSS_SELECTOR, ".b-list__main__title"
                    )
                    gp_elements = art.find_elements(
                        By.CSS_SELECTOR, ".b-list__summary__gp.b-gp"
                    )

                    # 共用：取 GP 文字
                    gp_text = self._parse_gp_text(gp_elements)
                    if gp_text is None:
                        print("此樓層找不到 GP 標籤，跳過")
                        continue

                    # 共用：轉成數值
                    gp_value = self._parse_gp_value(gp_text)

                    if gp_value > 15:
                        high_gp_post_titles.append(f"[{gp_value}] {title_elem.text}")

                    if gp_value > page_best_gp:
                        page_best_gp = gp_value
                        best_art_titles = title_elem

                except Exception as e:
                    print(f"這樓跳過了，原因：{e}")

        if best_art_titles:
            high_gp_post_titles.append(f"[{page_best_gp}] {best_art_titles.text}")
        return high_gp_post_titles


    def scan_high_gp_content(self, choice):
        high_gp_content = []
        page_best_gp = -1
        page_best_content = None

        posts = self.wait.until(
            EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, "section[id^='post_']")
            )
        )

        for post in posts:
            try:
                gp_elements = post.find_elements(By.CSS_SELECTOR, ".postgp")

                # 共用：取 GP 文字
                gp_text = self._parse_gp_text(gp_elements)
                if gp_text is None:
                    print("此樓層找不到 GP 標籤，跳過")
                    continue

                # 共用：轉成數值
                gp_value = self._parse_gp_value(gp_text)

                if gp_value == float("inf"):
                    content = post.find_element(
                        By.CSS_SELECTOR, ".c-article__content"
                    ).text
                    high_gp_content.append(f"[{gp_text}] {content}")
                    if choice == "1":
                        break

                else:
                    if gp_value > page_best_gp:
                        page_best_gp = gp_value
                        page_best_content = post.find_element(
                            By.CSS_SELECTOR, ".c-article__content"
                        ).text

            except Exception as e:
                print(f"這樓跳過了，原因：{e}")

        if page_best_content:
            high_gp_content.append(f"[{page_best_gp}] {page_best_content}")
        return high_gp_content
    
    
    def _parse_gp_text(self, elements): # 解析並針對 GP 處理
        '''取出 GP 元素的文字並去除空白'''
        if elements:           # 有東西才進來
            return elements[0].text.strip()
        else:
            return None

    def _parse_gp_value(self, gp_text): # 解析並針對爆文 GP 處理 
        '''把 gp_text 轉成數值，爆文回傳 inf'''
        if "爆" in gp_text:
            return float("inf")
        clean_gp = "".join(filter(str.isdigit, gp_text))
        return int(clean_gp) if clean_gp else 0
    
    
########################### 全部合併 function ###########################

    def scan_high_gp_post_and_title(self, find_type, choice):  # 取出巴哈文章標題
        """
        find_type 1 = 爬文章標題，其他的爬回覆文
        """
        high_gp_post_titles = []
        high_gp_content = []  # 最終要回傳的內容清單
        page_best_gp = -1  # 文章最少是 0，所以初始值給 -1 來比大小
        page_best_gp = -1  # 記錄目前找到的最高 GP 數值（預設 -1）
        best_art_titles = None
        page_best_content = None  # 對應最高 GP 的文章內容

        if find_type == 1:
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
                            if gp_value > 15:
                                high_gp_post_titles.append(f"[{gp_value}] {title_elem.text}")
                            
                            if gp_value > page_best_gp:
                                page_best_gp = gp_value
                                best_art_titles = title_elem

                    except Exception as e:
                        print(f"這樓跳過了，原因：{e}")  # 印出錯誤原因，但依然繼續跑下一輪

            if best_art_titles:
                high_gp_post_titles.append(f"[{page_best_gp}] {best_art_titles}")
            return (
                high_gp_post_titles  # 結論 : ["爆文 A 的內容", "爆文 B 的內容", "GP 最高一般文的內容"])
            )

        else:
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
                        if choice == "1":
                            high_gp_content.append(f"[{gp_text}] {page_best_content}")
                            break  # 第一筆爆文就停止
                        elif choice == "2":
                            high_gp_content.append(f"[{gp_text}] {page_best_content}")  # 繼續找下一篇爆文

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
                        By.CSS_SELECTOR, ".c-article__content").text
                
                except Exception as e:
                    print(f"這樓跳過了，原因：{e}")  # 印出錯誤原因，但依然繼續跑下一輪

            # 迴圈結束後，把 GP 最高的一般文章加進去
            if page_best_content:
                high_gp_content.append(f"[{page_best_gp}] {page_best_content}")
            return (
                high_gp_content  # 結論 : ["爆文 A 的內容", "爆文 B 的內容", "GP 最高一般文的內容"])
            )


    """
    未改前的版本，建議不要動
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
                            if gp_value > 15:
                                high_gp_post_titles.append(f"[{gp_value}] {title_elem.text}")
                            
                            if gp_value > page_best_gp:
                                page_best_gp = gp_value
                                best_art_titles = title_elem

                    except Exception as e:
                        print(f"這樓跳過了，原因：{e}")  # 印出錯誤原因，但依然繼續跑下一輪

            # return high_gp_post_titles, best_art_titles
            if best_art_titles:
                high_gp_post_titles.append(f"[{page_best_gp}] {best_art_titles}")
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
                    if choice == "1":
                        high_gp_content.append(f"[{gp_text}] {page_best_content}")
                        break  # 第一筆爆文就停止
                    elif choice == "2":
                        high_gp_content.append(f"[{gp_text}] {page_best_content}")  # 繼續找下一篇爆文

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
                    By.CSS_SELECTOR, ".c-article__content").text
            
            except Exception as e:
                print(f"這樓跳過了，原因：{e}")  # 印出錯誤原因，但依然繼續跑下一輪

        # 迴圈結束後，把 GP 最高的一般文章加進去
        if page_best_content:
            high_gp_content.append(f"[{page_best_gp}] {page_best_content}")
        return (
            high_gp_content  # 結論 : ["爆文 A 的內容", "爆文 B 的內容", "GP 最高一般文的內容"])
        )
        """
