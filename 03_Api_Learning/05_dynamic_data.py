import requests

# ============================================================
#  Dynamic Data
# ============================================================

# --- GET ---
url = "https://httpbin.org/base64/SFRUUEJJTiBpcyBhd2Vzb21l"

response = requests.get(url)

print(f"狀態碼: {response.status_code}")
print(f"回應內容: {response.text}")

# --- GET ---
url = "https://httpbin.org/delay/10" # 「打一個會慢 10 秒的 API，但我最多願意等 15 秒」

response = requests.get(url, timeout=15)

print(f"狀態碼: {response.status_code}")
print(f"回應內容: {response.text}")

