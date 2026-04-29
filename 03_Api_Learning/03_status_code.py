import requests

# ============================================================
#  Status Code（HTTP 狀態碼）
# ============================================================
# 3 位數狀態碼，告訴你請求結果：
#   2xx → 成功
#   3xx → 重新導向
#   4xx → 客戶端錯誤（你的請求有問題）
#   5xx → 伺服器錯誤
#
# 常見狀態碼：
#   200 OK             → 成功
#   201 Created        → 新增成功（POST 後常見）
#   204 No Content     → 成功但無內容（DELETE 後常見）
#   400 Bad Request    → 請求格式錯誤
#   401 Unauthorized   → 未驗證或驗證失敗
#   403 Forbidden      → 已驗證但沒權限
#   404 Not Found      → 資源不存在
#   500 Internal Error → 伺服器出問題
#
# 測試端點：https://httpbin.org/status/{codes}
# codes 填多個用逗號分隔時，伺服器會隨機回一個。

# ============================================================
# --- GET 200：讀取成功 ---
# ============================================================
get_url = "https://httpbin.org/status/200"

get_response = requests.get(
    get_url,
    json={"name": "Ryan", "email": "ryan@xxx.xxx.xxx"},
    timeout=5
)

print(f"[GET] 狀態碼: {get_response.status_code}")

# ============================================================
# --- POST 201：新增成功 ---
# ============================================================
# 201 比 200 更精確，表達「資源已建立」，設計良好的 API POST 後會這樣回
post_url = "https://httpbin.org/status/201"

post_response = requests.post(
    post_url,
    json={"name": "Ryan", "email": "ryan@xxx.xxx.xxx"},
    timeout=5
)

print(f"[POST] 狀態碼: {post_response.status_code}")

# ============================================================
# --- PUT 200：更新成功 ---
# ============================================================
put_url = "https://httpbin.org/status/200"

put_response = requests.put(
    put_url,
    json={"name": "Ryan", "email": "ryan@xxx.xxx.xxx"},
    timeout=5
)

print(f"[PUT] 狀態碼: {put_response.status_code}")

# ============================================================
# --- PATCH 200：部分更新成功 ---
# ============================================================
patch_url = "https://httpbin.org/status/200"

patch_response = requests.patch(
    patch_url,
    json={"email": "ryan@xxx.xxx.xxx"},
    timeout=5
)

print(f"[PATCH] 狀態碼: {patch_response.status_code}")

# ============================================================
# --- DELETE 204：刪除成功但無內容 ---
# ============================================================
# 204 規定不能帶 body，所以 .text 會是空字串、不能呼叫 .json()
delete_url = "https://httpbin.org/status/204"

delete_response = requests.delete(
    delete_url,
    timeout=5
)

print(f"[DELETE] 狀態碼: {delete_response.status_code}")

# ============================================================
# --- 多個狀態碼（隨機回傳）---
# ============================================================
# 用來測試「程式能否處理不同狀態碼」。實務上要依狀態碼分流：
#   if response.status_code == 200: ...
#   elif response.status_code == 404: ...
#   elif response.status_code >= 500: ...（可考慮重試）

random_url = "https://httpbin.org/status/200,404,500"

random_response = requests.get(
    random_url,
    timeout=5
)

print(f"[GET 隨機] 狀態碼: {random_response.status_code}")
