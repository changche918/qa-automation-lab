import requests

"""
20260420 用 API 取得文章標題 + 回覆文內容
    python xxxx --mode api/web --?? > 執行 API/執行爬蟲 (4/27之前) + AI schedule 掛起來
"""

# bsn=23805 是版代，snA=730010 是文章代號
# url_gamer_board = "https://forum.gamer.com.tw/C.php?bsn=23805&snA=730010&tnum=1"
url_gamer_board = "https://forum.gamer.com.tw/B.php?bsn=23805"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://www.gamer.com.tw/", # ← 模擬從首頁點進來
    "Accept-Language": "zh-TW,zh;q=0.9" # ← 多語系網站會看這個
}

response_gamer_content = requests.get(
    url_gamer_board,
    headers=headers
)

# print(response_gamer_content.text)
# with open("gamer_content.html", "w", encoding="utf-8") as f:
#     f.write(response_gamer_content.text)

# 想要的資料長這樣 : class="b-list__main__title">【閒聊】All max自選剩七天求建議</p>
# 要排除的資料 : class="b-list__row b-list__row--sticky b-list-item b-imglist-item">



html_text = response_gamer_content.text
rows = html_text.split('class="b-list__row')[1:]
results = []

for row in rows:
    tag_end = row.find(">")
    if 'b-list__row--sticky' in row[:tag_end]:
        continue

    # ── 標題 ──
    i = row.find('class="b-list__main__title"')
    if i == -1:
        continue
    start = row.find(">", i) + 1
    end = row.find("</p>", start)
    title = row[start:end].strip()

    # ── href（在 <p ...> 標籤內找）──
    p_open = row.rfind('<p', 0, i)                  # <p 開頭位置
    h = row.find('href="', p_open, start)           # 限制在這個 <p ...> 裡
    if h == -1:
        href = ""
    else:
        h_start = h + len('href="')
        h_end = row.find('"', h_start)
        href = "https://forum.gamer.com.tw/" + row[h_start:h_end]

    # ── GP ──
    g = row.find('class="b-list__summary__gp')
    if g == -1:
        gp = 0
    else:
        g_start = row.find(">", g) + 1
        g_end = row.find("</", g_start)
        gp = int(row[g_start:g_end].strip())        # ← 轉 int 才能比大小

    results.append({"title": title, "gp": gp, "href": href})

# ── 列出全部（可選）──
for idx, post in enumerate(results, 1):
    print(f"{idx}. [GP {post['gp']}] {post['title']}")

# ── 找 GP 最高的那篇 ──
top = max(results, key=lambda x: x["gp"])
print("\n=== GP 最高 ===")
print(f"標題：{top['title']}")
print(f"GP：{top['gp']}")
print(f"連結：{top['href']}")


url_gamer_content = top['href']

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://www.gamer.com.tw/", # ← 模擬從首頁點進來
    "Accept-Language": "zh-TW,zh;q=0.9" # ← 多語系網站會看這個
}

response_gamer_content_a = requests.get(
    url_gamer_content,
    headers=headers
)

# print(response_gamer_content_a.text)

with open("gamer_content.txt", "w", encoding="utf-8") as f:
    f.write(response_gamer_content_a.text)

# page = 1
# all_results = []

# while True:
#     params = {**base_params, "page": page}
#     resp = requests.get(BASE_URL, params=params, headers=HEADERS)
#     resp.raise_for_status()                   # 非 200 直接報錯

#     posts = parse_page(resp.text)             # 假設你的解析函式回傳 list
#     if not posts:                             # 空的 → 已經超過最後一頁
#         print(f"第 {page} 頁沒資料，結束")
#         break

#     print(f"✔ 第 {page} 頁：{len(posts)} 篇")
#     all_results.extend(posts)

#     page += 1
#     time.sleep(1)

