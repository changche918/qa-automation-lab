import requests

# ============================================================
#  Cookies
# ============================================================
# Cookie 是伺服器存在你這邊的小段資料，之後每次請求會自動帶上，
# 讓伺服器「記得你是誰」（登入狀態、偏好設定等）。

# ============================================================
# --- 主動帶 Cookie 給伺服器 ---
# ============================================================
# cookies=dict → requests 會把它組進 Cookie header 送出
# httpbin /cookies 會把收到的 cookie 原樣回傳，方便觀察

url = "https://httpbin.org/cookies"

response = requests.get(
    url, 
    cookies={"my_cookie": "hello"},
    timeout=5
)

print(f"狀態碼: {response.status_code}")
print(f"回應內容: {response.json()}")