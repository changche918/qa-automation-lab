import requests

# ============================================================
#  Response Formats（回應格式）
# ============================================================
# 伺服器回傳的內容可以是各種格式，用 Content-Type header 告訴你是什麼：
#   application/json      → JSON 格式（最常見，現代 API 首選）
#   text/html             → HTML 網頁
#   text/plain            → 純文字
#   image/png             → PNG 圖片
#   application/gzip      → 壓縮檔
#
# 「壓縮編碼」與「資料格式」是兩件不同的事：
#   資料格式（Content-Type）→ 資料的結構，例如 JSON
#   壓縮編碼（Content-Encoding）→ 傳輸時的壓縮方式，例如 gzip / brotli
# requests 會自動幫你解壓縮 gzip；brotli 需要額外安裝套件。

# ============================================================
# --- Brotli 壓縮格式 ---
# ============================================================
# Brotli 是 Google 開發的壓縮演算法，比 gzip 壓縮率更高，現代瀏覽器都支援。
# 需要安裝 brotli 套件才能讓 requests 自動解壓縮：pip install brotli
url = "https://httpbin.org/brotli"

# Accept-Encoding: br 告訴伺服器「我可以接受 brotli 壓縮」
# 伺服器若支援，就會壓縮後回傳，傳輸量更小
# 如果沒裝 brotli 套件，requests 無法自動解壓縮，會拋出例外
response = requests.get(url, headers={"Accept-Encoding": "br"})

print(f"狀態碼: {response.status_code}")
# .json() 等同於 json.loads(response.text)，把 JSON 字串轉成 Python dict
print(f"回應內容: {response.json()}")

# ============================================================
# --- JSON 格式（最常用）---
# ============================================================
# 現代 REST API 幾乎都用 JSON 格式回應。
# JSON 是一種用文字表達「結構化資料」的格式，Python 的 dict/list 可以和 JSON 互相轉換：
#   dict → JSON 字串：json.dumps(data)
#   JSON 字串 → dict：json.loads(text)  或直接用 response.json()
url = "https://httpbin.org/json"

response = requests.get(url)

print(f"狀態碼: {response.status_code}")
print(f"回應內容: {response.json()}")
# 取出特定欄位的兩種寫法：
# data = response.json()
# print(data["slideshow"]["title"])   ← 用 key 取值（key 不存在會拋 KeyError）
# print(data.get("slideshow", {}).get("title"))  ← 用 .get() 更安全，不存在時給預設值

# ============================================================
# 小結：讀取回應內容的方法比較
# ============================================================
# response.text      → 原始文字字串（適合 HTML、純文字）
# response.json()    → 自動解析成 Python dict/list（適合 JSON）
# response.content   → 原始 bytes（適合圖片、檔案下載）
# response.headers   → 回應的 HTTP headers（dict-like 物件）
