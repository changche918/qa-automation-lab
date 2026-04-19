import requests

# ============================================================
#  Redirects（重新導向）
# ============================================================
# 當伺服器回應 3xx 狀態碼，代表「你要的東西在別的地方，請去那裡找」。
# 瀏覽器和 requests 預設都會自動跟著跳轉。
#
# 常見 3xx 狀態碼：
#   301 Moved Permanently  → 永久搬家，書籤請更新（SEO 常用）
#   302 Found              → 暫時搬家，下次還是來這裡
#   303 See Other          → POST 後導到 GET 頁面（表單送出後跳轉）
#   307 Temporary Redirect → 暫時跳轉，且保留原本的 HTTP 方法
#   308 Permanent Redirect → 永久跳轉，且保留原本的 HTTP 方法
#
# 這個端點 /absolute-redirect/10 會連續跳轉 10 次，最後才到達目的地。
# requests 預設允許最多 30 次跳轉，超過會拋出 TooManyRedirects 例外。

# ============================================================
# --- 自動跟著跳轉（預設行為）---
# ============================================================
url = "https://httpbin.org/absolute-redirect/10"

# requests 預設 allow_redirects=True，會自動跟完所有跳轉才回傳最終結果
response = requests.get(url)

print(f"狀態碼: {response.status_code}")  # 最終會是 200（跳轉完的結果）
print(f"經過了幾次跳轉: {len(response.history)}")  # response.history 儲存每一次跳轉的 Response
print(f"回應內容: {response.text}")

# ============================================================
# 進階用法：控制跳轉行為
# ============================================================
# 不自動跳轉，只看第一層回應：
# response = requests.get(url, allow_redirects=False)
# print(response.status_code)  # 302
# print(response.headers["Location"])  # 下一個目的地 URL

# 限制最多跳轉次數（避免被惡意 API 無限跳轉）：
# session = requests.Session()
# session.max_redirects = 5  # 最多 5 次，超過拋 TooManyRedirects
# response = session.get(url)

# 查看完整跳轉路徑：
# for r in response.history:
#     print(f"  {r.status_code} → {r.headers.get('Location')}")
# print(f"最終: {response.url}")
