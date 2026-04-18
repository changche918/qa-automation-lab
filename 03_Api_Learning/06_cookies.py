import requests

# ============================================================
#  Cookies
# ============================================================

# --- 查看 cookie ---
url = "https://httpbin.org/cookies"

response = requests.get(url, cookies={"my_cookie": "hello"})

print(f"狀態碼: {response.status_code}")
print(f"回應內容: {response.json()}")

# --- 請 Server 設定 cookie，再刪除 cookie ---
# 使用 Session 讓 cookie 可以跨請求保留
session = requests.Session()

url = "https://httpbin.org/cookies/set"
response = session.get(url, params={"my_cookie": "hello"}, allow_redirects=True)

print(f"狀態碼: {response.status_code}")
print(f"回應內容: {response.json()}")

url = "https://httpbin.org/cookies/delete"
response = session.get(url, params={"my_cookie": ""}, allow_redirects=True)

print(f"狀態碼: {response.status_code}")
print(f"回應內容: {response.json()}")
