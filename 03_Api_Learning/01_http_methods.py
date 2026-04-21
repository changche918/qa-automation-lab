import requests

# ============================================================
#  HTTP Methods
# ============================================================
# 不同「動詞」代表不同意圖：
#   GET    → 讀取資料
#   POST   → 新增資料
#   PUT    → 完整取代（沒傳的欄位會變空）
#   PATCH  → 部分更新（只改指定欄位）
#   DELETE → 刪除資料
#
# httpbin.org 會把你送出的請求原封不動回傳，方便觀察實際送了什麼。

# ============================================================
# --- GET ---
# ============================================================
print("=== GET ===")
get_url = "https://httpbin.org/get"

# 兩種寫法等價：
#   requests.get(get_url)                ← 簡潔（最常用）
#   requests.request("GET", get_url)     ← 通用（適合動態決定方法)

# 20260420 有空抽 function 看看
get_response = requests.request(
    "GET",
    get_url,
    headers={},
    timeout=5
)

print(get_response)
print(f"狀態碼: {get_response.status_code}")
print(f"內容類型: {get_response.headers.get('Content-Type')}")
print(f"回應內容:\n{get_response.text}")

# ============================================================
# --- POST ---
# ============================================================
# 傳資料的兩種參數：
#   json={...}  → Content-Type = application/json（現代 API）
#   data={...}  → Content-Type = application/x-www-form-urlencoded（表單）
print("=== POST ===")
post_url = "https://httpbin.org/post"

post_response = requests.post(
    post_url,
    json={"name": "Ryan"},
    timeout=5
)

print(post_response)
print(f"狀態碼: {post_response.status_code}")
print(f"內容類型: {post_response.headers.get('Content-Type')}")
print(f"回應內容:\n{post_response.text}")

# ============================================================
# --- DELETE ---
# ============================================================
# 慣例：要刪的資源 ID 放 URL 裡，不帶 body
# 例如 requests.delete("https://api.example.com/users/123")
delete_url = "https://httpbin.org/delete"

delete_response = requests.delete(
    delete_url,
    timeout=5
)

print(delete_response)
print(f"狀態碼: {delete_response.status_code}")
print(f"內容類型: {delete_response.headers.get('Content-Type')}")
print(f"回應內容:\n{delete_response.text}")

# ============================================================
# --- PATCH ---
# ============================================================
# PATCH 與 PUT 的差異：PATCH 只改指定欄位，PUT 是整筆覆蓋
patch_url = "https://httpbin.org/patch"

patch_response = requests.patch(
    patch_url,
    json={"email": "new@example.com"},
    timeout=5
)

print(patch_response)
print(f"狀態碼: {patch_response.status_code}")
print(f"內容類型: {patch_response.headers.get('Content-Type')}")
print(f"回應內容:\n{patch_response.text}")

# ============================================================
# --- PUT ---
# ============================================================
# 完整覆蓋：沒傳的欄位會被清空，所以實務上要送「整筆」資料
put_url = "https://httpbin.org/put"

put_response = requests.put(
    put_url,
    json={"name": "Ryan", "email": "ryan@xxx.xxx.xxx"},
    timeout=5
)

print(put_response)
print(f"狀態碼: {put_response.status_code}")
print(f"內容類型: {put_response.headers.get('Content-Type')}")
print(f"回應內容:\n{put_response.text}")
