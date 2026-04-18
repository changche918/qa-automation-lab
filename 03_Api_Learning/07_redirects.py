import requests

# ============================================================
#  Redirects
# ============================================================

# --- GET ---
url = "https://httpbin.org/absolute-redirect/10"

response = requests.get(url)

print(f"狀態碼: {response.status_code}")
print(f"回應內容: {response.text}")