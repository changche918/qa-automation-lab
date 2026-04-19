import requests

# ============================================================
#  Auth（身分驗證）
# ============================================================
# API 通常需要驗證「你是誰」才能存取資料，常見有兩種方式：
#
#   1. Basic Auth（基本驗證）：帳號 + 密碼，最簡單，安全性較低
#      → 帳密會被 Base64 編碼後放進 Authorization header 傳送
#      → 一定要搭配 HTTPS，否則帳密幾乎等於明文
#
#   2. Bearer Token（令牌驗證）：用一組 token 代替帳密，主流做法
#      → 通常先用帳密換取 token（如 OAuth 登入流程），之後每次用 token 驗證
#      → token 可以設定期限、權限範圍，比帳密更安全、更靈活

# ============================================================
# --- Basic Auth 範例 ---
# ============================================================
# URL 裡直接帶了帳號（myuser）和密碼（mypassword），這是 httpbin 的測試端點設計。
# 實際 API 不會把帳密放在 URL，而是用 auth 參數傳遞。
url = "https://httpbin.org/basic-auth/myuser/mypassword"

# auth=("帳號", "密碼") 是 requests 的快捷語法
# requests 會自動幫你把帳密轉成 Base64 並放進 Authorization header：
#   Authorization: Basic bXl1c2VyOm15cGFzc3dvcmQ=
response = requests.get(url, auth=("myuser", "mypassword"))

print(f"狀態碼: {response.status_code}")  # 200 = 驗證成功；401 = 驗證失敗
print(f"回應內容: {response.json()}")     # .json() 把 JSON 字串轉成 Python dict，方便取值

# ============================================================
# --- Bearer Token 範例 ---
# ============================================================
# Bearer Token 是現代 API 最常見的驗證方式（例如 GitHub API、OpenAI API）。
# token 通常從「登入 API」或「API 金鑰管理頁面」取得，要妥善保管不要洩漏。
url = "https://httpbin.org/bearer"
token = "my-secret-token"

# 手動把 token 放進 Authorization header，格式固定為 "Bearer <token>"
# 沒有快捷語法，必須自己組 headers dict 傳入
response = requests.get(url, headers={"Authorization": f"Bearer {token}"})

print(f"狀態碼: {response.status_code}")  # 200 = token 有效；401 = token 無效或過期
print(f"回應內容: {response.json()}")

# ============================================================
# 小結：兩種驗證方式比較
# ============================================================
# Basic Auth：
#   優點 → 設定簡單，一行搞定
#   缺點 → 每次都傳帳密，一旦洩漏就很危險；無法設定權限範圍或有效期限
#
# Bearer Token：
#   優點 → 可設有效期限、可依需求給予不同權限、可隨時撤銷單一 token
#   缺點 → 需要先有取得 token 的流程（登入 or 申請 API key）
