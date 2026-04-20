import requests
# from requests.auth import HTTPBasicAuth  # ← 若要用下面「等價寫法」才需要 import

# ============================================================
#  Auth（身分驗證）
# ============================================================
# 常見兩種方式：
#   1. Basic Auth：帳密會被 Base64 編碼放進 Authorization header
#                  → Base64 不是加密，一定要搭配 HTTPS
#   2. Bearer Token：用 token 代替帳密，主流做法，可設期限與權限範圍

# ============================================================
# --- Basic Auth 範例（成功） ---
# ============================================================
# /basic-auth/{user}/{pass} 端點會比對你送來的帳密是否跟 URL 裡相同
basic_url = "https://httpbin.org/basic-auth/myuser/mypassword"

# auth=("帳號", "密碼") 是快捷語法，requests 會自動組 Authorization header
basic_response = requests.get(
    basic_url,
    auth=("myuser", "mypassword"),
    timeout=5
)

print("--- Basic Auth 成功 ---")
print(f"狀態碼: {basic_response.status_code}")
print(f"送出的 Authorization: {basic_response.request.headers['Authorization']}")
# ↑ Basic bXl1c2VyOm15cGFzc3dvcmQ= ← Base64 編碼後的帳密
print(f"回應內容: {basic_response.json()}")

# 等價寫法（語意完全相同）：
# basic_response = requests.get(basic_url, auth=HTTPBasicAuth("myuser", "mypassword"), timeout=5)

# ============================================================
# --- Basic Auth 範例（失敗） ---
# ============================================================
basic_fail_response = requests.get(
    basic_url,
    auth=("myuser", "wrongpassword"),
    timeout=5
)

print("\n--- Basic Auth 失敗 ---")
print(f"狀態碼: {basic_fail_response.status_code}")  # 401 Unauthorized
print(f"回應內容: {basic_fail_response.text!r}")     # 失敗 body 是空字串，用 !r 才看得出

# ============================================================
# --- Bearer Token 範例（成功） ---
# ============================================================
# 沒有快捷語法，要自己組 Authorization header，格式固定為 "Bearer <token>"
bearer_url = "https://httpbin.org/bearer"
token = "my-secret-token"

bearer_response = requests.get(
    bearer_url,
    headers={"Authorization": f"Bearer {token}"},
    timeout=5
)

print("\n--- Bearer Token 成功 ---")
print(f"狀態碼: {bearer_response.status_code}")
print(f"回應內容: {bearer_response.json()}")

# ============================================================
# --- Bearer Token 範例（失敗） ---
# ============================================================
# 不帶 Authorization header，模擬沒登入或 token 過期
bearer_fail_response = requests.get(
    bearer_url,
    timeout=5
)

print("\n--- Bearer Token 失敗 ---")
print(f"狀態碼: {bearer_fail_response.status_code}")  # 401
print(f"回應內容: {bearer_fail_response.text!r}")
