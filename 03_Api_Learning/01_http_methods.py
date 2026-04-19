import requests

# ============================================================
#  HTTP Methods
# ============================================================
# HTTP 是瀏覽器與伺服器溝通的規則，不同「動詞」代表不同意圖：
#   GET    → 讀取資料（不改變伺服器狀態）
#   POST   → 新增資料
#   PUT    → 完整取代資料（整筆覆蓋）
#   PATCH  → 部分更新資料（只改指定欄位）
#   DELETE → 刪除資料
#
# 使用 httpbin.org 這個測試用 API，它會把你送出的請求原封不動地回給你，
# 方便學習時觀察「你送出了什麼」。

# ============================================================
# --- GET ---
# ============================================================
# GET 是最常見的方法，用來「取得」資料，不應該有任何副作用（不改資料）。
url = "https://httpbin.org/get"

# 寫法一：簡潔寫法（最常用）
# response = requests.get(url)

# 寫法二：通用寫法 requests.request()
# 好處：方法名稱用字串傳入，適合動態決定 HTTP 方法的場合（例如從設定檔讀取）
# headers={} 代表不帶任何自訂標頭
# timeout=5  代表最多等 5 秒，超過就拋出例外，避免程式無限等待
response = requests.request(
    "GET",
    "https://httpbin.org/get",
    headers={},
    timeout=5
)

print(response)                                          # 印出 Response 物件，例如 <Response [200]>
print(f"狀態碼: {response.status_code}")                # 200 = 成功；4xx = 客戶端錯誤；5xx = 伺服器錯誤
print(f"內容類型: {response.headers.get('Content-Type')}") # 告訴你回應是 JSON、HTML 還是圖片等
print(f"回應內容:\n{response.text}")                    # 純文字格式的回應內容

# ============================================================
# --- POST ---
# ============================================================
# POST 用來「新增」資料，通常會附帶 body（請求主體），把新資料傳給伺服器。
# 實際應用：填表單送出、建立新用戶、上傳資料等。
url = "https://httpbin.org/post"

# 常見寫法：加上 json= 或 data= 傳送資料
# requests.post(url, json={"name": "Ryan"})  ← 傳 JSON，Content-Type 自動設為 application/json
# requests.post(url, data={"name": "Ryan"})  ← 傳表單，Content-Type 為 application/x-www-form-urlencoded
response = requests.post(url)  # 這裡沒帶 body，只是示範方法本身

print(response)
print(f"狀態碼: {response.status_code}")
print(f"內容類型: {response.headers.get('Content-Type')}")
print(f"回應內容:\n{response.text}")

# ============================================================
# --- DELETE ---
# ============================================================
# DELETE 用來「刪除」資源，通常在 URL 裡帶上要刪除的資源 ID。
# 實際應用：requests.delete("https://api.example.com/users/123")
url = "https://httpbin.org/delete"

response = requests.delete(url)

print(response)
print(f"狀態碼: {response.status_code}")
print(f"內容類型: {response.headers.get('Content-Type')}")
print(f"回應內容:\n{response.text}")

# ============================================================
# --- PATCH ---
# ============================================================
# PATCH 用來「部分更新」資源，只傳你要改的欄位，其餘欄位保持原樣。
# 與 PUT 的差異：PUT 是整筆覆蓋，沒傳的欄位會變空；PATCH 只改你指定的欄位。
# 實際應用：requests.patch(url, json={"email": "new@example.com"})  ← 只改 email
url = "https://httpbin.org/patch"

response = requests.patch(url)

print(response)
print(f"狀態碼: {response.status_code}")
print(f"內容類型: {response.headers.get('Content-Type')}")
print(f"回應內容:\n{response.text}")

# ============================================================
# --- PUT ---
# ============================================================
# PUT 用來「完整取代」資源，必須傳入完整的資料，沒傳的欄位會被清空。
# 實際應用：requests.put(url, json={"name": "Ryan", "email": "ryan@example.com"})
url = "https://httpbin.org/put"

response = requests.put(url)

print(response)
print(f"狀態碼: {response.status_code}")
print(f"內容類型: {response.headers.get('Content-Type')}")
print(f"回應內容:\n{response.text}")
