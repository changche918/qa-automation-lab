import requests


# 20260423 改為純 API 版；保留兩個方法：scan_high_gp_post_api / scan_high_gp_content_api
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}


class FindHighGP:
    def __init__(self):
        """API 版不需要瀏覽器驅動，建構子不接任何參數"""
        pass

    def scan_high_gp_post_api(self, url):
        """
        掃文章列表頁，取出 GP > 15 的文章、本頁 GP 最高的文章，並回傳最高 GP 文章的完整網址

        參數:
        - url: str, 文章列表頁網址
        回傳:
        - tuple(list[str], str|None)
          - list[str]: 例 ["[爆] 標題A", "[35] 標題B", "[35] 本頁最高 GP 標題"]
          - str|None: 本頁 GP 最高文章的完整網址，若沒有文章則為 None
        """
        # 1. 抓網頁 HTML
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        html_text = resp.text

        high_gp_post_titles = []
        page_best_gp = -1
        page_best_title = None
        page_best_href = None

        # 2. 以每個文章 row 的 class 開頭當切點，把 HTML 切成一篇一篇
        rows = html_text.split('class="b-list__row')[1:]

        # 3. 逐篇處理
        for row in rows:
            # 3-1. 只在 row 的開頭 <div ...> 標籤內檢查，有 --sticky 代表置頂文，跳過
            tag_end = row.find(">")
            if 'b-list__row--sticky' in row[:tag_end]:
                continue

            # 3-2. 抓標題：從 class="b-list__main__title" 後的 > 到 </p>
            post_title = row.find('class="b-list__main__title"')
            if post_title == -1:
                continue
            post_title_start = row.find(">", post_title) + 1
            post_title_end = row.find("</p>", post_title_start)
            title = row[post_title_start:post_title_end].strip()

            # 3-3. 抓 GP 文字：class 可能是 --good / --bad / --zero，只比對前綴
            post_gp = row.find('class="b-list__summary__gp')
            if post_gp == -1:
                continue
            post_gp_start = row.find(">", post_gp) + 1
            post_gp_end = row.find("</", post_gp_start)
            gp_text = row[post_gp_start:post_gp_end].strip()

            # 3-4. 把 GP 文字換算成可以比較大小的數值
            if "爆" in gp_text:
                gp_value = float("inf")
            else:
                clean_gp = "".join(filter(str.isdigit, gp_text))
                gp_value = int(clean_gp) if clean_gp else 0

            # 3-5. GP > 15 的文章收進清單（爆文 inf 也符合）
            if gp_value > 15:
                display = gp_text if gp_value == float("inf") else gp_value
                high_gp_post_titles.append(f"[{display}] {title}")

            # 3-6. 追蹤本頁最高 GP 的文章，並抓它的 href（在 title 位置之前往回找最近的 href="..."）
            if gp_value > page_best_gp:
                page_best_gp = gp_value
                page_best_title = title
                post_href = row.rfind('href="', 0, post_title)
                if post_href != -1:
                    post_href_start = post_href + len('href="')
                    post_href_end = row.find('"', post_href_start)
                    page_best_href = row[post_href_start:post_href_end]

        # 4. 迴圈跑完後，把本頁最高 GP 的文章補進清單
        if page_best_title:
            display = "爆" if page_best_gp == float("inf") else page_best_gp
            high_gp_post_titles.append(f"[{display}] {page_best_title}")

        # 5. 把相對路徑補上網域，變成完整網址（href 可能是 "C.php?..." 相對路徑）
        best_art_url = None
        if page_best_href:
            if page_best_href.startswith("http"):
                best_art_url = page_best_href
            else:
                best_art_url = f"https://forum.gamer.com.tw/{page_best_href}"
               #  https://forum.gamer.com.tw/C.php?bsn=23805&snA=730010&tnum=1

        return high_gp_post_titles, best_art_url

    def scan_high_gp_content_api(self, url, choice):
        """
        掃文章頁回覆，取出爆文回覆與本頁 GP 最高的一般回覆

        參數:
        - url: str, 文章頁網址（可含 page= 分頁）
        - choice: str, "1" 只抓第一筆爆文；"2" 抓所有爆文
        回傳:
        - tuple(list[str], bool), 例：(["[爆] 內文A", "[35] 內文B"], True)
          第二個值代表「是否還有下一頁」，給主程式決定要不要繼續換頁
        """
        # 1. 抓網頁 HTML
        resp = requests.get(url, headers=HEADERS)
        html_text = resp.text

        # 2. 判斷是否還有下一頁：
        #    巴哈 HTML 的引號會混用 —— 啟用按鈕是 class='next'（單引號），停用是 class="next no"（雙引號）
        #    所以兩種引號都要檢查
        next_enabled = 'class="next"' in html_text or "class='next'" in html_text
        next_disabled = 'class="next no"' in html_text or "class='next no'" in html_text
        has_next = next_enabled and not next_disabled

        high_gp_content = []
        page_best_gp = -1
        page_best_content = None

        # 3. 每個回覆樓層的 <section> 都帶 id="post_xxx"，用 id="post_ 當切點
        #    （巴哈實際 HTML 是 <section class="c-section"  id="post_xxx">，class 在 id 之前）
        posts = html_text.split('id="post_')[1:]

        # 4. 逐樓處理
        for post in posts:
            # 4-1. 抓 GP 文字
            content_gp = post.find('class="postgp"')
            if content_gp == -1:
                print("此樓層找不到 GP 標籤，跳過")
                continue
            content_gp_start = post.find(">", content_gp) + 1
            content_gp_end = post.find("</", content_gp_start)
            gp_text = post[content_gp_start:content_gp_end].strip()

            # 4-2. 抓內文：從 class="c-article__content" 後的 > 開始
            #      內文會有多個巢狀 <div>（巴哈把每一段包在 <div> 裡），不能只抓第一個 </div>
            #      要用「深度計數」找出 c-article__content 這個外層 div 的配對結束標籤：
            #      每碰到一個 <div 深度 +1；每碰到一個 </div> 深度 -1；歸零時就是配對位置
            post_content = post.find('class="c-article__content')
            if post_content == -1:
                continue
            post_content_start = post.find(">", post_content) + 1

            depth = 1
            pos = post_content_start
            post_content_end = post_content_start
            while depth > 0:
                next_open = post.find("<div", pos)
                next_close = post.find("</div>", pos)
                if next_close == -1:
                    post_content_end = len(post)
                    break
                if next_open != -1 and next_open < next_close:
                    depth += 1
                    pos = next_open + len("<div")
                else:
                    depth -= 1
                    if depth == 0:
                        post_content_end = next_close
                    pos = next_close + len("</div>")
            raw_content = post[post_content_start:post_content_end]

            # 4-3. 把 HTML 標籤拿掉，只留下純文字
            content = ""
            in_tag = False
            for ch in raw_content:
                if ch == "<":
                    in_tag = True
                elif ch == ">":
                    in_tag = False
                elif not in_tag:
                    content += ch
            content = " ".join(content.split())  # 壓縮連續空白

            # 4-4. 爆文：直接加入清單
            if "爆" in gp_text:
                high_gp_content.append(f"[{gp_text}] {content}")
                if choice == "1":
                    break
                continue

            # 4-5. 一般樓層：只保留本頁 GP 最高的那一筆
            clean_gp = "".join(filter(str.isdigit, gp_text))
            gp_value = int(clean_gp) if clean_gp else 0
            if gp_value > page_best_gp:
                page_best_gp = gp_value
                page_best_content = content

        # 5. 迴圈跑完後，把本頁 GP 最高的一般回覆補進清單
        if page_best_content:
            high_gp_content.append(f"[{page_best_gp}] {page_best_content}")

        return high_gp_content, has_next
