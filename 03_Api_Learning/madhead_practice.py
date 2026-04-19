import requests

# ============================================================
#  巴哈姆特神魔之塔版 → 爬取討論版文章
# ============================================================
# 這是一個「非官方爬蟲」範例，示範如何對一般網站（非 REST API）發送請求。
# 巴哈不提供公開 API，所以我們要模擬瀏覽器行為才能成功取得資料。
#
# 為什麼需要模擬瀏覽器？
# 很多網站會偵測請求的 User-Agent，如果發現不是瀏覽器（例如 Python-urllib），
# 就會拒絕或回傳空內容，防止自動化爬取。

# ============================================================
# --- 目標 URL ---
# ============================================================
# 巴哈神魔之塔討論版，bsn=23805 是版代，snA=730010 是文章代號
# url_gamer = "https://forum.gamer.com.tw/B.php?bsn=23805"  # 版面首頁（已備用，未使用）
url_gamer_content = "https://forum.gamer.com.tw/C.php?bsn=23805&snA=730010&tnum=1"

# ============================================================
# --- 自訂 Headers（關鍵步驟）---
# ============================================================
# User-Agent：告訴伺服器「我是 Chrome 瀏覽器」，讓伺服器以為是正常使用者在瀏覽。
# 沒有這個 header，很多網站會直接拒絕或回傳錯誤。
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    # 以下是可選的進階 headers，有些網站需要才能成功取得資料：
    # "Referer": "https://www.gamer.com.tw/"
    # → 告訴伺服器「我是從首頁點進來的」，模擬正常瀏覽行為，某些站會檢查這個
    #
    # "Origin": "https://www.gamer.com.tw"
    # → 跨域請求（CORS）才需要，一般爬蟲不用
    #
    # "Accept": "application/json, text/plain, */*"
    # → 告訴伺服器你可以接受哪些回應格式，爬 HTML 網頁通常不需要指定
    #
    # "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    # → 告訴伺服器你偏好繁體中文，對多語系網站有用
}

# ============================================================
# --- 發送請求 ---
# ============================================================
# response_gamer = requests.get(url_gamer, headers=headers)  # 版面首頁（備用，已註解）
response_gamer_content = requests.get(url_gamer_content, headers=headers)

print(f"狀態碼: {response_gamer_content.status_code}")
# 200 = 成功取得 HTML；403 = 被擋；429 = 爬太快被限速

# response.text 取得 HTML 原始碼
# 實際上要「解析」HTML 內容，通常會用 BeautifulSoup 套件：
#   from bs4 import BeautifulSoup
#   soup = BeautifulSoup(response_gamer_content.text, "html.parser")
#   posts = soup.select(".c-section")  # 用 CSS selector 找文章區塊
print(response_gamer_content.text)

# ============================================================
# 爬蟲注意事項：
# ============================================================
# 1. 請遵守目標網站的 robots.txt（https://forum.gamer.com.tw/robots.txt）
# 2. 請控制請求頻率（加上 time.sleep(1) 等），避免對伺服器造成負擔
# 3. 部分網站禁止爬蟲，請先確認使用條款是否允許
# 4. 若網站有提供官方 API，優先使用 API 而非直接爬 HTML
