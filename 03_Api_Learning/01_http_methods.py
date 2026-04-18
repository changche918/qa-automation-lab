import requests

# ============================================================
#  HTTP Methods
# ============================================================
 
# --- GET ---
url = "https://httpbin.org/get" # 1. 定義 API 網址

# response = requests.get(url) # 2. 發出請求 
response = requests.request(
    "GET",
    "https://httpbin.org/get",
    headers={},
    timeout=5
)
 
print(response)
print(f"狀態碼: {response.status_code}")
print(f"內容類型: {response.headers.get('Content-Type')}")
print(f"回應內容:\n{response.text}")

# --- POST ---
url = "https://httpbin.org/post"

response = requests.post(url)
 
print(response)
print(f"狀態碼: {response.status_code}")
print(f"內容類型: {response.headers.get('Content-Type')}")
print(f"回應內容:\n{response.text}")

# --- DELETE ---
url = "https://httpbin.org/delete"

response = requests.delete(url)
 
print(response)
print(f"狀態碼: {response.status_code}")
print(f"內容類型: {response.headers.get('Content-Type')}")
print(f"回應內容:\n{response.text}")

# --- PATCH ---
url = "https://httpbin.org/patch"

response = requests.patch(url)
 
print(response)
print(f"狀態碼: {response.status_code}")
print(f"內容類型: {response.headers.get('Content-Type')}")
print(f"回應內容:\n{response.text}")

# --- PUT ---
url = "https://httpbin.org/put"

response = requests.put(url)
 
print(response)
print(f"狀態碼: {response.status_code}")
print(f"內容類型: {response.headers.get('Content-Type')}")
print(f"回應內容:\n{response.text}")