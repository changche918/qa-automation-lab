import requests

"""
20260420 用 API 取得文章標題 + 回覆文內容
    python xxxx --mode api/web --?? > 執行 API/執行爬蟲 (4/27之前) + AI schedule 掛起來
"""

# bsn=23805 是版代，snA=730010 是文章代號
# url_gamer_content = "https://forum.gamer.com.tw/C.php?bsn=23805&snA=730010&tnum=1"
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

# print(f"狀態碼: {response_gamer_content.status_code}")
# print(response_gamer_content.text)

html_text = response_gamer_content.text
results = []

rows = html_text.split('class="b-list__row')[1:]   # 每塊是一篇文章

for row in rows:
    if 'b-list__row--sticky' in row[:200]:    # 只看開頭一小段判斷
        continue
    i = row.find('class="b-list__main__title"')
    if i == -1:
        continue
    start = row.find(">", i) + 1
    end = row.find("</p>", start)
    results.append(row[start:end].strip())


# 想要的資料長這樣 : class="b-list__main__title">【閒聊】All max自選剩七天求建議</p>
# 要排除的資料 : class="b-list__row b-list__row--sticky b-list-item b-imglist-item"
# chunks = html_text.split('class="b-list__main__title"')

# mode = "post"
# for chunk in chunks[1:]:
#     start = chunk.find(">") + 1 # 找到 > 和 </p> 之間的文字就是標題
#     end = chunk.find("</p>")
#     title = chunk[start:end]
#     results.append(title)

    count = 1
for post_title in results:
    print(f"{count}.{post_title}")
    count += 1
