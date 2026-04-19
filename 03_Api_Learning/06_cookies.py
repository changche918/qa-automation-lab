import requests

# ============================================================
#  Cookies
# ============================================================
# Cookie 是伺服器存在你瀏覽器（或客戶端）裡的一小段資料，
# 之後每次請求都會自動帶上，讓伺服器「記得你是誰」。
#
# 常見用途：
#   - 維持登入狀態（Session Cookie）
#   - 記住使用者偏好（語言、深色模式）
#   - 追蹤使用者行為（廣告分析）
#
# Cookie 的生命週期：
#   - Session Cookie：關閉瀏覽器就消失（無設定過期時間）
#   - Persistent Cookie：有明確的過期日期，關閉瀏覽器也保留

# ============================================================
# --- 主動帶 Cookie 給伺服器 ---
# ============================================================
# 用 cookies 參數傳入一個 dict，requests 會把它加進 Cookie header 送出。
# 伺服器（httpbin）收到後，會把你帶過去的 cookie 原封不動地回給你，方便觀察。
url = "https://httpbin.org/cookies"

response = requests.get(url, cookies={"my_cookie": "hello"})

print(f"狀態碼: {response.status_code}")
print(f"回應內容: {response.json()}")  # 可以看到 cookies 欄位裡有你送出的值

# ============================================================
# --- 使用 Session 跨請求保留 Cookie ---
# ============================================================
# 問題：一般的 requests.get() 每次都是獨立的，不會記住上次的 cookie。
# 解法：用 requests.Session() 建立一個「會話」，它會自動儲存並帶上 cookie，
#       模擬瀏覽器的登入後連線行為。
#
# Session 的好處：
#   1. 自動保留 cookie（不用每次手動帶）
#   2. 可以設定共用的 headers（例如 Authorization token）
#   3. 底層使用連線池，多次請求效能更好
session = requests.Session()

# 步驟 1：請伺服器幫我設定一個 cookie
# params={"my_cookie": "hello"} 等同於在 URL 加上 ?my_cookie=hello（Query String）
# allow_redirects=True 代表自動跟著伺服器的 3xx 跳轉（/cookies/set 會先 302 導到 /cookies）
url = "https://httpbin.org/cookies/set"
response = session.get(url, params={"my_cookie": "hello"}, allow_redirects=True)

print(f"狀態碼: {response.status_code}")
print(f"回應內容: {response.json()}")  # 應該看到 cookie 已被設定
print(f"Session 裡的 cookies: {dict(session.cookies)}")  # 查看 session 目前保存的 cookies

# 步驟 2：請伺服器刪除這個 cookie
# 傳空字串給該 cookie key，httpbin 就會把它刪掉
url = "https://httpbin.org/cookies/delete"
response = session.get(url, params={"my_cookie": ""}, allow_redirects=True)

print(f"狀態碼: {response.status_code}")
print(f"回應內容: {response.json()}")  # cookie 應該已不存在
