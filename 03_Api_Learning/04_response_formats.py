import requests

# ============================================================
#  Response Formats
# ============================================================

# --- GET ---
url = "https://httpbin.org/brotli"

# 需要安裝 brotli 套件才能自動解壓縮：pip install brotli
response = requests.get(url, headers={"Accept-Encoding": "br"})

print(f"狀態碼: {response.status_code}")
print(f"回應內容: {response.json()}")

# --- GET ---
url = "https://httpbin.org/json"

response = requests.get(url)

print(f"狀態碼: {response.status_code}")
print(f"回應內容: {response.json()}")