import requests


# 20260422 改為純 API 版，移除 selenium；僅保留兩個方法：掃文章列表 / 掃回覆內容
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
        掃文章列表頁，取出 GP > 15 的文章與本頁 GP 最高的文章

        參數:
        - url: str, 文章列表頁網址
        回傳:
        - list[str], 例：["[爆] 標題A", "[35] 標題B", "[35] 本頁最高 GP 標題"]
        """
        # 取得 HTML
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        html_text = resp.text

        high_gp_post_titles = []
        page_best_gp = -1
        page_best_title = None

        # 以每個 row 的 class 開頭為切點，切成每篇文章的 HTML 片段
        rows = html_text.split('class="b-list__row')[1:]

        for row in rows:
            # 只在該 row 的開頭 <div ...> 標籤內檢查是否為置頂文
            tag_end = row.find(">")
            if 'b-list__row--sticky' in row[:tag_end]:
                continue

            # 抓標題：從 class="b-list__main__title" 後的 > 到 </p>
            i = row.find('class="b-list__main__title"')
            if i == -1:
                continue
            t_start = row.find(">", i) + 1
            t_end = row.find("</p>", t_start)
            title = row[t_start:t_end].strip()

            # 抓 GP：class 可能是 --good / --bad / --zero，只比對前綴
            g = row.find('class="b-list__summary__gp')
            if g == -1:
                continue
            g_start = row.find(">", g) + 1
            g_end = row.find("</", g_start)
            gp_text = row[g_start:g_end].strip()

            # 把 GP 文字換算成可以比較大小的數值
            if "爆" in gp_text:
                gp_value = float("inf")
            else:
                clean_gp = "".join(filter(str.isdigit, gp_text))
                gp_value = int(clean_gp) if clean_gp else 0

            # GP > 15 的文章收進清單（爆文 inf 也符合）
            if gp_value > 15:
                display = gp_text if gp_value == float("inf") else gp_value
                high_gp_post_titles.append(f"[{display}] {title}")

            # 追蹤本頁最高 GP 的文章
            if gp_value > page_best_gp:
                page_best_gp = gp_value
                page_best_title = title

        # 迴圈跑完後，把本頁最高 GP 的文章補進清單
        if page_best_title:
            display = "爆" if page_best_gp == float("inf") else page_best_gp
            high_gp_post_titles.append(f"[{display}] {page_best_title}")

        return high_gp_post_titles

    def scan_high_gp_content_api(self, url, choice):
        """
        掃文章頁回覆，取出爆文回覆與本頁 GP 最高的一般回覆

        參數:
        - url: str, 文章頁網址（可含 page= 分頁）
        - choice: str, "1" 只抓第一筆爆文；"2" 抓所有爆文
        回傳:
        - tuple(list[str], bool),
          (高 GP 回覆清單, 是否還有下一頁)
        """
        # 取得 HTML
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        html_text = resp.text

        # 判斷是否還有下一頁：有 class="next" 且不是停用狀態 class="next no"
        has_next = 'class="next"' in html_text and 'class="next no"' not in html_text

        high_gp_content = []
        page_best_gp = -1
        page_best_content = None

        # 每個回覆樓層以 <section id="post_xxx"> 開頭，用它當切點
        posts = html_text.split('<section id="post_')[1:]

        for post in posts:
            # 抓 GP 文字
            g = post.find('class="postgp"')
            if g == -1:
                print("此樓層找不到 GP 標籤，跳過")
                continue
            g_start = post.find(">", g) + 1
            g_end = post.find("</", g_start)
            gp_text = post[g_start:g_end].strip()

            # 抓內文起點：class="c-article__content" 後面那個 > 的下一個位置
            c = post.find('class="c-article__content')
            if c == -1:
                continue
            c_start = post.find(">", c) + 1

            # 找內文結束位置：內文可能有巢狀 <div>（引用、圖片等），
            # 所以要追蹤 <div> 的開關深度，找到對應的 </div>
            depth = 1
            pos = c_start
            c_end = c_start
            while pos < len(post):
                next_open = post.find("<div", pos)
                next_close = post.find("</div>", pos)
                if next_close == -1:
                    break
                # 遇到內層 <div>，深度 +1，繼續往後找
                if next_open != -1 and next_open < next_close:
                    depth += 1
                    pos = next_open + 4
                else:
                    # 遇到 </div>，深度 -1；深度歸零代表就是外層對應的收尾
                    depth -= 1
                    if depth == 0:
                        c_end = next_close
                        break
                    pos = next_close + 6

            raw_content = post[c_start:c_end]

            # 把 HTML 標籤拿掉，只留下純文字
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

            # 爆文：直接加入清單
            if "爆" in gp_text:
                high_gp_content.append(f"[{gp_text}] {content}")
                if choice == "1":
                    break
                continue

            # 一般樓層：只保留本頁 GP 最高的那一筆
            clean_gp = "".join(filter(str.isdigit, gp_text))
            gp_value = int(clean_gp) if clean_gp else 0
            if gp_value > page_best_gp:
                page_best_gp = gp_value
                page_best_content = content

        # 迴圈跑完後，把本頁 GP 最高的一般回覆補進清單
        if page_best_content:
            high_gp_content.append(f"[{page_best_gp}] {page_best_content}")

        return high_gp_content, has_next
