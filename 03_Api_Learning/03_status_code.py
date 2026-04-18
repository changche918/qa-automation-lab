import requests

# ============================================================
#  Status Code
# ============================================================
# 端點格式：https://httpbin.org/status/{codes}
# 支援方法：GET, POST, PUT, DELETE, PATCH
# codes 可以填單一狀態碼，也可以填多個（用逗號分隔），多個時會隨機回傳其中一個

# --- GET ---
url = "https://httpbin.org/status/200"
response = requests.get(url)
print(f"[GET] 狀態碼: {response.status_code}")

# --- POST ---
url = "https://httpbin.org/status/201"
response = requests.post(url)
print(f"[POST] 狀態碼: {response.status_code}")

# --- PUT ---
url = "https://httpbin.org/status/200"
response = requests.put(url)
print(f"[PUT] 狀態碼: {response.status_code}")

# --- PATCH ---
url = "https://httpbin.org/status/200"
response = requests.patch(url)
print(f"[PATCH] 狀態碼: {response.status_code}")

# --- DELETE ---
url = "https://httpbin.org/status/204"
response = requests.delete(url)
print(f"[DELETE] 狀態碼: {response.status_code}")

# --- 隨機回傳（多個狀態碼用逗號分隔）---
url = "https://httpbin.org/status/200,404,500"
response = requests.get(url)
print(f"[GET 隨機] 狀態碼: {response.status_code}")